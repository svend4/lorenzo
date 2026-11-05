---
date: 2026-06-05
tags: [memory, rag, orchestration, ingestion, architecture]
state: normalized
---

# Парсинг PDF-отчётов публичных компаний для трейдерских инсайтов

<!-- toc-auto -->
<!-- tags: llm-financial-pdf-analytics-pipeline, docs -->


<!-- summary -->
> Парсинг PDF-отчётов публичных компаний для трейдерских инсайтов — раздел документации проекта Lorenzo.
 
 
 
>   — раздел документации проекта Lorenzo.


> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

**Автор:** ovchinnikovproger (Amvera, Хабр, сентябрь 2025)  
**Хабр:** https://habr.com/ru/companies/amvera/articles/949966/  
**GitHub:** https://github.com/user11415926535-dot/Parser_2  
**Слой:** ingestion / analytics  
**Дата:** сентябрь 2025  
**Уникальность:** Полный end-to-end pipeline: автоматическое скачивание PDF с сайтов публичных компаний → PyMuPDF extraction → LLaMA 8B с двумя режимами промптинга (структурированные метрики: выручка/EBITDA + регуляторные риски) → asyncio + Telegram рассылка. Реальный GitHub + работающий код на живых финансовых отчётах.

## Задача: автоматический анализ финансовых отчётов

```
Инвестор / трейдер вручную:
  → Зайти на сайт компании → найти отчёт (IR-раздел)
  → Скачать PDF 200+ страниц
  → Прочитать (1-2 часа)
  → Извлечь ключевые цифры
  → Написать вывод

Автоматизация через LLM:
  → Автоматически обнаружить IR-страницы публичных компаний
  → Скачать PDF (правильные URL через эвристики)
  → Извлечь текст без OCR (PyMuPDF)
  → LLM анализирует: метрики + риски
  → Telegram-рассылка за <1 минуты
```

## Этап 1: Discovery — нахождение финансовых отчётов

```python
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin

class FinancialReportDiscovery:
    """
    Автоматически находить страницы IR и ссылки на финансовые PDF.
    """

    # Паттерны URL для финансовых отчётов (эвристика)
    PDF_URL_PATTERNS = [
        r'annual[-_]report',
        r'годовой[-_]отчет',
        r'financial[-_]statement',
        r'отчетность',
        r'МСФО|IFRS|РСБУ|GAAP',
        r'(?:Q[1-4]|H[12])\d{4}',   # Q1-2025, H1-2025
    ]

    IR_PAGE_KEYWORDS = [
        'investor relations', 'инвесторам',
        'акционерам', 'раскрытие информации',
        'отчётность', 'финансовые результаты'
    ]

    def find_ir_pdf_links(self, company_website: str) -> list[str]:
        """Найти ссылки на финансовые PDF на сайте компании."""
        response = requests.get(company_website, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        pdf_links = []
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            link_text = a_tag.get_text(strip=True).lower()

            # Фильтр: ссылка на PDF и содержит финансовые ключевые слова
            if href.endswith('.pdf') and any(
                re.search(p, href + link_text, re.IGNORECASE)
                for p in self.PDF_URL_PATTERNS
            ):
                pdf_links.append(urljoin(company_website, href))

        return pdf_links

    def build_company_watchlist(self, companies: list[str]) -> dict:
        """Сформировать watchlist: компания → список PDF."""
        return {
            company: self.find_ir_pdf_links(website)
            for company, website in companies
        }
```

## Этап 2: Извлечение текста из PDF (PyMuPDF)

```python
import fitz  # PyMuPDF

class PDFTextExtractor:
    """
    PyMuPDF: быстрое извлечение текста без OCR.
    Работает с цифровыми PDF (большинство публичных компаний).
    Ограничение: сканированные документы требуют OCR.
    """

    def extract(self, pdf_url: str) -> str:
        """Скачать PDF и извлечь текст."""
        # Скачать в память (не сохранять на диск)
        response = requests.get(pdf_url, timeout=30)
        doc = fitz.open(stream=response.content, filetype="pdf")

        pages_text = []
        for page_num, page in enumerate(doc):
            text = page.get_text("text")

            # Пропустить служебные страницы (оглавление, обложка)
            if len(text.strip()) < 100:
                continue

            pages_text.append(f"[Страница {page_num + 1}]\n{text}")

        return "\n\n".join(pages_text)

    def extract_relevant_sections(self, full_text: str) -> str:
        """
        Финансовые отчёты огромны (200+ страниц).
        Извлечь только релевантные секции для LLM.
        """
        FINANCIAL_SECTIONS = [
            "финансовые результаты", "выручка", "ebitda",
            "чистая прибыль", "долговая нагрузка",
            "ключевые показатели", "риски", "прогноз"
        ]

        paragraphs = full_text.split('\n\n')
        relevant = [
            p for p in paragraphs
            if any(kw in p.lower() for kw in FINANCIAL_SECTIONS)
        ]

        # Ограничение контекста LLM: первые ~8000 слов
        return "\n\n".join(relevant)[:32000]
```

## Этап 3: Двойной режим промптинга LLaMA 8B

```python
from openai import OpenAI

class FinancialLLMAnalyzer:
    """
    Два разных промпта для двух типов анализа:
    1. Структурированное извлечение метрик (числа)
    2. Качественный анализ рисков (регуляторика, рынок)
    """

    def __init__(self, api_base: str = "http://localhost:8000/v1"):
        self.client = OpenAI(base_url=api_base)  # совместимо с vLLM

    METRICS_PROMPT = """Ты — финансовый аналитик. Извлеки ключевые метрики из отчёта.

Верни ТОЛЬКО JSON в формате:
{{
  "period": "Q1 2025 | H1 2025 | FY 2024",
  "revenue_bln_rub": <число или null>,
  "ebitda_bln_rub": <число или null>,
  "net_income_bln_rub": <число или null>,
  "net_debt_ebitda": <число или null>,
  "revenue_yoy_pct": <число или null>,
  "guidance": "<прогноз компании или null>"
}}

Фрагмент отчёта:
{text}"""

    RISK_PROMPT = """Ты — риск-аналитик. Найди регуляторные и рыночные риски.

Верни ТОЛЬКО JSON:
{{
  "regulatory_risks": ["<риск 1>", "<риск 2>"],
  "market_risks": ["<риск 1>"],
  "management_commentary": "<ключевая цитата руководства>",
  "sentiment": "positive | neutral | negative"
}}

Фрагмент отчёта:
{text}"""

    def analyze_metrics(self, text: str) -> dict:
        """Структурированное извлечение финансовых метрик."""
        response = self.client.chat.completions.create(
            model="llama-8b",
            messages=[{
                "role": "user",
                "content": self.METRICS_PROMPT.format(text=text[:8000])
            }],
            response_format={"type": "json_object"},
            temperature=0.1  # детерминированный вывод для чисел
        )
        return json.loads(response.choices[0].message.content)

    def analyze_risks(self, text: str) -> dict:
        """Качественный анализ рисков и комментарии менеджмента."""
        response = self.client.chat.completions.create(
            model="llama-8b",
            messages=[{
                "role": "user",
                "content": self.RISK_PROMPT.format(text=text[8000:16000])
            }],
            response_format={"type": "json_object"},
            temperature=0.3
        )
        return json.loads(response.choices[0].message.content)
```

## Этап 4: Async Pipeline + Telegram рассылка

```python
import asyncio
import aiohttp
from telethon import TelegramClient

class FinancialReportPipeline:
    """
    Полный async pipeline: скачать → извлечь → анализировать → опубликовать.
    """

    async def process_company(self, company: str,
                               pdf_url: str) -> AnalysisResult:
        """Обработать один PDF отчёт."""
        async with aiohttp.ClientSession() as session:
            # Скачать PDF
            async with session.get(pdf_url) as resp:
                pdf_bytes = await resp.read()

        # Извлечь текст (CPU-bound → thread pool)
        text = await asyncio.get_event_loop().run_in_executor(
            None, self.extractor.extract_from_bytes, pdf_bytes
        )

        # LLM анализ (параллельно!)
        metrics, risks = await asyncio.gather(
            asyncio.get_event_loop().run_in_executor(
                None, self.analyzer.analyze_metrics, text
            ),
            asyncio.get_event_loop().run_in_executor(
                None, self.analyzer.analyze_risks, text
            )
        )

        return AnalysisResult(company=company, metrics=metrics, risks=risks)

    async def run_watchlist(self, watchlist: dict) -> list[AnalysisResult]:
        """Обработать все компании из watchlist параллельно."""
        tasks = [
            self.process_company(company, url)
            for company, urls in watchlist.items()
            for url in urls
        ]
        return await asyncio.gather(*tasks, return_exceptions=True)

    async def publish_to_telegram(self, results: list[AnalysisResult],
                                   channel_id: str):
        """Опубликовать результаты в Telegram-канал."""
        async with TelegramClient('bot', self.api_id, self.api_hash) as client:
            for result in results:
                message = self._format_message(result)
                await client.send_message(channel_id, message, parse_mode='md')
                await asyncio.sleep(1)  # anti-flood

    def _format_message(self, r: AnalysisResult) -> str:
        m = r.metrics
        return (
            f"**{r.company}**\n"
            f"Период: {m.get('period', 'н/д')}\n"
            f"Выручка: {m.get('revenue_bln_rub', 'н/д')} млрд ₽ "
            f"({m.get('revenue_yoy_pct', '?')}% г/г)\n"
            f"EBITDA: {m.get('ebitda_bln_rub', 'н/д')} млрд ₽\n"
            f"Чистый долг/EBITDA: {m.get('net_debt_ebitda', 'н/д')}x\n"
            f"Настроение: {r.risks.get('sentiment', '?')}\n"
            f"Риски: {', '.join(r.risks.get('regulatory_risks', [])[:2])}"
        )
```

## Применение к Lorenzo

```python
# improve_financial_monitor.py (паттерн):

class LorenzoFinancialMonitor:
    """
    Lorenzo мониторит OSS-проекты. Аналогия:
    вместо финансовых PDF → статьи Хабра / GitHub релизы.
    Тот же pipeline: discover → extract → LLM analyze → notify.
    """

    async def monitor_habr_author(self, habr_username: str) -> AuthorReport:
        # Stage 1: найти новые статьи автора
        new_articles = await self.habr_api.get_recent(habr_username, days=7)

        # Stage 2: извлечь текст (requests + BS4)
        texts = await asyncio.gather(*[
            self.extract_article(url) for url in new_articles
        ])

        # Stage 3: LLM анализ (метрики + новинки)
        analyses = await asyncio.gather(*[
            self.analyzer.analyze_tech_update(text) for text in texts
        ])

        return AuthorReport(author=habr_username, updates=analyses)
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **FinPDF + IDP+VLM (R30)** | VLM для сканированных отчётов плохого качества (PDFs с печатями) |
| **FinPDF + LLM Judge (R28)** | Judge верифицирует извлечённые числа (нет галлюцинаций в суммах) |
| **FinPDF + Synthetic Data (R30)** | Синтетические финансовые отчёты для тестирования pipeline |
| **FinPDF + Enterprise RAG (R32)** | Корпоративная БЗ = все проанализированные отчёты + Q&A поверх |
| **FinPDF + CAVM Analytics (R26)** | CAVM обогащает числа → FinPDF pipeline даёт входные данные |

## Контакт

- Статья: https://habr.com/ru/companies/amvera/articles/949966/ (сентябрь 2025)
- GitHub: https://github.com/user11415926535-dot/Parser_2
- Amvera: amvera.ru (облако для Python ML приложений)
- Смежная (Finam FinBench, бенчмарки RU финансовых LLM): https://habr.com/ru/companies/finam_broker/articles/989842/
- Смежная (финансовый AI-агент MCP+CodeAct): https://habr.com/ru/articles/980542/
- PyMuPDF: github.com/pymupdf/PyMuPDF (AGPL)

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
- [Решения](../../../DECISIONS.md)
