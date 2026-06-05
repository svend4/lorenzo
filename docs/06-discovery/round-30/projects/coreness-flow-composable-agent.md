# Coreness Flow: локальный AI-агент с plug-in архитектурой и горячей перезагрузкой

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

**Автор:** Vensus (Хабр, март 2025)  
**Хабр:** https://habr.com/ru/articles/1005176/  
**GitHub:** не опубликован (личный проект, архитектура детально описана)  
**Слой:** orchestration / memory / knowledge  
**Дата:** март 2025  
**Уникальность:** Десктопный AI-агент с системой автообнаружения плагинов: каждый плагин = папка с `config.json` + Python-модуль, без явной регистрации. Трёхслойная API шина (UI/Backend/Bus) с hot-reload без перезапуска: смена модели или API-ключа — мгновенная замена клиента. YAML-сценарии для мультишаговых пайплайнов без изменения кода. Локальный RAG: BGE-M3 ONNX + встроенный Qdrant.

## Проблема монолитных AI-агентов

```
Монолитный агент (типичный):
  Хочешь сменить модель:  → Правки в config.py + restart
  Хочешь добавить фичу:   → Правки в core + риск сломать всё
  Хочешь новый инструмент: → Зарегистрировать в реестре вручную
  Хочешь сценарий:        → Написать код

Composable агент (Coreness Flow):
  Сменить модель:         → Изменить settings.json → auto hot-reload
  Добавить фичу:          → Положить папку с plugin → auto-discovery
  Новый инструмент:       → config.json декларирует → auto-register
  Новый сценарий:         → YAML файл → без кода
```

## Архитектура: трёхслойная API шина

```
┌─────────────────────────────────────────────────────────┐
│  UI Layer (Frontend)                                     │
│  → React/Tauri десктоп                                   │
│  → Не знает о плагинах напрямую                          │
└──────────────────────┬──────────────────────────────────┘
                       │ API calls
┌──────────────────────▼──────────────────────────────────┐
│  Bus Layer (Event Bus)                                   │
│  → Маршрутизация событий между UI и Backend              │
│  → Подписка плагинов на события                          │
│  → Hot-reload: плагин перезагружается без restart        │
└──────────────────────┬──────────────────────────────────┘
                       │ plugin calls
┌──────────────────────▼──────────────────────────────────┐
│  Backend Layer (Plugin Host)                             │
│  → Auto-discovery: сканирует plugins/ при старте         │
│  → Регистрирует плагины из config.json                   │
│  → Управляет lifecycle каждого плагина                   │
└─────────────────────────────────────────────────────────┘
```

## Plugin Discovery: без явной регистрации

```python
# Структура плагина (всё что нужно):
# plugins/openai_chat/
#   config.json
#   plugin.py

# config.json (декларативно):
PLUGIN_CONFIG_EXAMPLE = {
    "name": "openai_chat",
    "version": "1.2.0",
    "provides": ["chat", "completion"],
    "requires": {
        "env": ["OPENAI_API_KEY"],
        "config": ["model", "temperature"]
    },
    "hot_reload": True,  # поддерживает горячую замену
    "priority": 10       # при конфликте имён побеждает больший
}

# plugin.py (минимальный контракт):
class Plugin:
    def on_load(self, config: dict) -> None:
        self.client = OpenAI(api_key=config["OPENAI_API_KEY"])
        self.model = config.get("model", "gpt-4o")

    def on_reload(self, new_config: dict) -> None:
        """Hot-reload: пересоздать клиент с новыми настройками"""
        self.client = OpenAI(api_key=new_config["OPENAI_API_KEY"])
        self.model = new_config.get("model", "gpt-4o")
        # Без restart! on_reload вызывается при изменении settings.json

    def chat(self, messages: list[dict]) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )
        return response.choices[0].message.content


# PluginHost: автообнаружение при старте
class PluginHost:
    def discover(self, plugins_dir: str) -> None:
        for plugin_dir in Path(plugins_dir).iterdir():
            config_path = plugin_dir / "config.json"
            if config_path.exists():
                config = json.loads(config_path.read_text())
                module = importlib.import_module(f"plugins.{plugin_dir.name}.plugin")
                plugin = module.Plugin()
                plugin.on_load(config)
                self.register(config["provides"], plugin)
                # Никакой явной регистрации — просто положи папку!
```

## Hot-Reload: мгновенная смена модели

```python
# Пользователь меняет модель в UI → settings.json обновляется →
# FileWatcher замечает → PluginHost перезагружает плагин

class SettingsWatcher:
    def __init__(self, settings_path: str, host: PluginHost):
        self.observer = Observer()
        self.observer.schedule(
            SettingsEventHandler(host),
            path=settings_path,
            recursive=False
        )

class SettingsEventHandler(FileSystemEventHandler):
    def on_modified(self, event):
        new_settings = json.loads(Path(event.src_path).read_text())

        # Найти затронутые плагины
        for plugin_name, plugin in self.host.plugins.items():
            if plugin.config_changed(new_settings):
                plugin.on_reload(new_settings)
                # → Клиент пересоздан с новым API-ключом или моделью
                # → Пользователь видит новую модель в следующем запросе
                # → Никакого restart, никакой потери состояния

# Практика:
# OpenAI API → Anthropic API: изменить 1 параметр → мгновенно
# GPT-4o → GPT-4o-mini: изменить model → мгновенно
# Добавить новый инструмент: положить папку → авто-регистрация
```

## YAML-сценарии: пайплайны без кода

```yaml
# scenarios/research_pipeline.yaml
name: "Research Pipeline"
description: "Найти, проанализировать, написать отчёт"

steps:
  - id: search
    plugin: web_search
    action: search
    input:
      query: "{{ user_query }}"
      max_results: 10

  - id: summarize
    plugin: openai_chat
    action: summarize
    input:
      texts: "{{ search.results }}"
    depends_on: [search]

  - id: classify
    plugin: local_classifier
    action: classify_relevance
    input:
      items: "{{ summarize.output }}"
    depends_on: [summarize]

  - id: write_report
    plugin: openai_chat
    action: write_report
    condition: "{{ classify.relevant_count > 3 }}"
    input:
      data: "{{ classify.relevant_items }}"
    depends_on: [classify]

# Добавить новый сценарий = создать yaml файл
# Изменить шаг = отредактировать yaml
# Нет кода!
```

## Локальный RAG: BGE-M3 + Qdrant без облака

```python
# RAG-плагин (пример плагина с собственным хранилищем)

class LocalRAGPlugin:
    def on_load(self, config: dict) -> None:
        # BGE-M3 через ONNX: не нужен PyTorch, работает везде
        self.encoder = ORTModelForFeatureExtraction.from_pretrained(
            "BAAI/bge-m3",
            export=True,
            provider="CPUExecutionProvider"  # CPU-only, без GPU
        )

        # Встроенный Qdrant: in-process, без отдельного сервера
        self.qdrant = QdrantClient(":memory:")
        self.qdrant.create_collection(
            "docs",
            vectors_config=VectorParams(size=1024, distance=Distance.COSINE)
        )

    def add_document(self, text: str, metadata: dict) -> None:
        embedding = self.encode(text)
        self.qdrant.upsert("docs", points=[
            PointStruct(id=uuid4().int, vector=embedding, payload=metadata)
        ])

    def search(self, query: str, top_k: int = 5) -> list[dict]:
        query_embedding = self.encode(query)
        results = self.qdrant.search("docs", query_embedding, limit=top_k)
        return [r.payload for r in results]

# Всё локально: BGE-M3 ONNX (CPU) + Qdrant in-memory
# Без облака, без Docker, без GPU
```

## Применение к Lorenzo

Lorenzo скрипты = "плагины" без системы обнаружения. Coreness Flow паттерн:

```python
# improve_plugin_host.py (паттерн):

class LorenzoPluginHost:
    """
    Аналог PluginHost: каждый improve_*.py = плагин
    Auto-discovery вместо явного списка в improve_run_all.py
    """
    PLUGINS_DIR = Path("scripts/")

    def discover(self) -> dict[str, ScriptPlugin]:
        plugins = {}
        for script in self.PLUGINS_DIR.glob("improve_*.py"):
            # Читать docstring как config
            config = self.parse_script_config(script)
            if config:
                plugins[config.name] = ScriptPlugin(
                    path=script,
                    group=config.group,
                    provides=config.outputs,
                    requires=config.inputs
                )
        return plugins

    def parse_script_config(self, script: Path) -> ScriptConfig:
        """Извлечь метаданные из docstring скрипта"""
        tree = ast.parse(script.read_text())
        docstring = ast.get_docstring(tree)
        if docstring and "group:" in docstring:
            return parse_yaml_docstring(docstring)
        return None

    # → improve_run_all.py больше не нужен статический список
    # → новый скрипт = просто положить в scripts/
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **Coreness Flow + MCP (R04)** | Каждый MCP-инструмент = плагин: auto-discovery без конфига |
| **Coreness Flow + LLM Router (R20)** | Роутер выбирает плагин: локальная модель или облако |
| **Coreness Flow + Durable State (R23)** | Plugin state сохраняется между reload через SessionContext |
| **Coreness Flow + Skills Library (R27)** | Skills Library = набор плагинов для оркестратора |
| **Coreness Flow + Personal AI (R27)** | Персональный AI = набор плагинов: health, finance, calendar |

## Контакт

- Статья: https://habr.com/ru/articles/1005176/ (март 2025)
- Смежная (MLOps composable pipeline): https://habr.com/ru/companies/ruvds/articles/1013854/
- BGE-M3 (multilingual embeddings): github.com/FlagOpen/FlagEmbedding
- Qdrant (vector DB): github.com/qdrant/qdrant (Apache 2.0)
- ONNX Runtime: github.com/microsoft/onnxruntime (MIT)
