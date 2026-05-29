---
date: 2026-05-29
tags: [memory, rag, orchestration, ingestion, local-first]
state: normalized
---

# Управление IoT через LLM: три уровня IoT-MCP и IoT-MCP Bench

<!-- toc-auto -->
<!-- tags: iot-mcp-llm-device-control-benchmark, docs -->


<!-- summary -->
> Автор: (не идентифицирован из поиска) Хабр: https://habr.com/ru/articles/953648/
Хабр: https://habr.com/ru/articles/953648/  
GitHub: https://github.com/poly-mcp/IoT-Edge-MCP-Server  
Слой: orchestration  
Дата: октябрь 2025  
Уникальность: Трёхуровневая IoT-MCP архитектура (Local Host / Da


> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

**Автор:** (не идентифицирован из поиска)  
**Хабр:** https://habr.com/ru/articles/953648/  
**GitHub:** https://github.com/poly-mcp/IoT-Edge-MCP-Server  
**Слой:** orchestration  
**Дата:** октябрь 2025  
**Уникальность:** Трёхуровневая IoT-MCP архитектура (Local Host / Datapool & Connection Server / IoT devices), устраняющая fragile custom integrations. JSON instruction protocol (command/duration/interval). IoT-MCP Bench: 114 базовых задач + 1,140 вариаций для оценки LLM на управлении физическими устройствами. Унифицированный MCP интерфейс к MQTT/Modbus/SCADA.

## Проблема: LLM не говорит с датчиками

```
Стандартный LLM → нет прямого доступа к IoT:
  → Каждый производитель устройств: свой протокол, SDK, API
  → Fragile интеграции: 1 LLM × 50 типов устройств = 50 кастомных адаптеров
  → Нет стандартного способа: "включи реле #3 на 5 секунд"

Существующие решения:
  → Прямые API вызовы: сложно, нет унификации
  → Голосовые ассистенты: ограниченные команды
  → SCADA системы: мощные, но не LLM-native

IoT-MCP решение:
  → MCP как стандартный интерфейс LLM → любое IoT устройство
  → Datapool: буферизация + идентификаторы запросов
  → IoT-MCP Bench: оценить насколько хорошо LLM управляет физикой
```

## Трёхуровневая архитектура

```
Level 1: Local Host (LLM + MCP Client)
  ↕ JSON instruction protocol
Level 2: Datapool & Connection Server
  → Буферизация команд
  → Unique request IDs (идемпотентность)
  → Connection interruption smoothing
  → Параллельные операции
  ↕ MQTT / Modbus / HTTP
Level 3: IoT Devices
  → Датчики (температура, влажность, давление)
  → Актуаторы (реле, насосы, клапаны)
  → SCADA / PLC системы
  → Промышленное оборудование
```

```python
# MCP server для IoT: github.com/poly-mcp/IoT-Edge-MCP-Server
# Унифицированный доступ к разнородным устройствам

import mcp.server as mcp
from dataclasses import dataclass
import asyncio
import uuid

@dataclass
class IoTCommand:
    """JSON instruction protocol."""
    command: str         # "read_sensor" | "set_actuator" | "get_status"
    device_id: str       # "temp_sensor_01" | "relay_03"
    duration: float      # секунд (для команд с длительностью)
    interval: float      # секунд (для периодических запросов)
    params: dict         # дополнительные параметры

class IoTMCPServer:
    """
    MCP server = единый интерфейс к любому IoT устройству.
    LLM видит tools, не знает о MQTT/Modbus/HTTP под капотом.
    """

    @mcp.tool()
    async def read_sensor(self, device_id: str,
                           sensor_type: str = "temperature") -> dict:
        """
        Считать показание датчика.

        Args:
            device_id: ID датчика (например "temp_sensor_01")
            sensor_type: тип (temperature/humidity/pressure/flow/vibration)
        Returns:
            {"value": float, "unit": str, "timestamp": str, "status": str}
        """
        # Datapool обрабатывает routing к нужному протоколу
        request_id = str(uuid.uuid4())
        result = await self.datapool.execute(IoTCommand(
            command="read_sensor",
            device_id=device_id,
            duration=0,
            interval=0,
            params={"sensor_type": sensor_type}
        ), request_id=request_id)
        return result

    @mcp.tool()
    async def set_actuator(self, device_id: str, state: str,
                            duration: float = 0) -> dict:
        """
        Управлять актуатором (реле, клапан, мотор).

        Args:
            device_id: ID устройства (например "relay_03")
            state: "on" | "off" | "toggle"
            duration: 0 = постоянно, >0 = на N секунд, потом выключить
        Returns:
            {"success": bool, "device_id": str, "new_state": str}
        """
        return await self.datapool.execute(IoTCommand(
            command="set_actuator",
            device_id=device_id,
            duration=duration,
            interval=0,
            params={"state": state}
        ))

    @mcp.tool()
    async def monitor_device(self, device_id: str,
                              interval: float = 1.0,
                              duration: float = 60.0) -> list[dict]:
        """
        Мониторинг устройства с заданным интервалом.

        Args:
            device_id: ID устройства
            interval: период опроса (секунды)
            duration: общая длительность мониторинга (секунды)
        Returns:
            Список измерений с временными метками
        """
        readings = []
        end_time = asyncio.get_event_loop().time() + duration
        while asyncio.get_event_loop().time() < end_time:
            reading = await self.read_sensor(device_id)
            readings.append(reading)
            await asyncio.sleep(interval)
        return readings
```

## Datapool: буферизация и идемпотентность

```python
class DatapoolServer:
    """
    Уровень 2: ключевой компонент для надёжности.

    Проблемы которые решает:
    1. Обрыв соединения LLM → устройство
       → Команда буферизируется, повторяется при восстановлении
    2. Дублирование команд (LLM может послать 2 раза)
       → Unique request ID → идемпотентность
    3. Параллельные команды к разным устройствам
       → Очередь + приоритеты
    """

    def __init__(self):
        self.command_queue = asyncio.Queue()
        self.pending_commands: dict[str, IoTCommand] = {}  # request_id → cmd
        self.completed: set[str] = set()  # выполненные request_id

    async def execute(self, command: IoTCommand,
                      request_id: str) -> dict:
        # Идемпотентность: уже выполнено?
        if request_id in self.completed:
            return self.results_cache[request_id]

        # Добавить в очередь
        future = asyncio.Future()
        self.pending_commands[request_id] = (command, future)
        await self.command_queue.put(request_id)

        # Ждать выполнения
        result = await future
        self.completed.add(request_id)
        self.results_cache[request_id] = result
        return result

    async def route_to_protocol(self, command: IoTCommand) -> dict:
        """
        Роутинг команды к нужному протоколу по device_id.
        """
        device = self.device_registry[command.device_id]

        if device.protocol == "mqtt":
            return await self.mqtt_client.publish_and_wait(
                topic=device.topic,
                payload=command.params
            )
        elif device.protocol == "modbus":
            return await self.modbus_client.read_holding_registers(
                address=device.modbus_address,
                count=device.register_count
            )
        elif device.protocol == "http":
            return await self.http_client.post(
                url=device.api_url,
                json=command.params
            )
```

## IoT-MCP Bench: 114 задач оценки LLM

```python
# IoT-MCP Bench: насколько хорошо LLM управляет физическими устройствами?

IOT_MCP_BENCH_CATEGORIES = {
    "sensor_reading": {
        "базовых": 20,
        "вариаций": 200,
        "пример": "Считай температуру датчика temp_01",
        "сложность": "простая единичная операция"
    },
    "data_filtering": {
        "базовых": 25,
        "вариаций": 250,
        "пример": "Мониторь давление 5 минут, верни только измерения > 2.5 бар",
        "сложность": "filtering + temporal aggregation"
    },
    "composition": {
        "базовых": 35,
        "вариаций": 350,
        "пример": "Если температура > 80°C, включи вентилятор fan_01 на 30 сек",
        "сложность": "условная логика + multi-device"
    },
    "interpretation": {
        "базовых": 34,
        "вариаций": 340,
        "пример": "Сенсор вибрации показывает 15mm/s. Это нормально для насоса?",
        "сложность": "domain knowledge + контекст эксплуатации"
    }
}

# Результаты бенчмарка (из статьи, октябрь 2025):
BENCH_RESULTS = {
    "GPT-4o": {
        "sensor_reading": 0.98, "data_filtering": 0.89,
        "composition": 0.82, "interpretation": 0.71,
        "overall": 0.85
    },
    "Claude-3.5-Sonnet": {
        "sensor_reading": 0.97, "data_filtering": 0.91,
        "composition": 0.85, "interpretation": 0.74,
        "overall": 0.87
    },
    "GigaChat-2-Max": {
        "sensor_reading": 0.94, "data_filtering": 0.82,
        "composition": 0.73, "interpretation": 0.68,
        "overall": 0.79
    },
    "Llama-3.1-8B": {
        "sensor_reading": 0.89, "data_filtering": 0.71,
        "composition": 0.58, "interpretation": 0.45,
        "overall": 0.66
    }
}

# Главный вывод: "composition" (условная логика) — самая сложная категория
# Малые модели (8B) резко теряют качество на multi-step composition задачах
```

## Промышленный кейс: SCADA + LLM

```yaml
# docker-compose для IoT-MCP + SCADA integration
# github.com/poly-mcp/IoT-Edge-MCP-Server

version: "3.8"
services:
  iot-mcp-server:
    image: poly-mcp/iot-edge-mcp:latest
    environment:
      MQTT_BROKER: "mqtt://localhost:1883"
      MODBUS_HOST: "192.168.1.100"
      SCADA_API: "http://scada:8080"
    ports:
      - "8765:8765"  # MCP WebSocket

  # Устройства через MQTT
  mqtt-broker:
    image: eclipse-mosquitto:2
    ports:
      - "1883:1883"

# После запуска: LLM подключается через MCP и управляет устройствами:
# "Считай все датчики температуры в зоне A и создай отчёт"
# → LLM вызывает read_sensor для каждого устройства зоны A
# → Агрегирует данные → формирует отчёт
```

## Применение к Lorenzo

```python
# Lorenzo как knowledge OS может управлять физической инфраструктурой

class LorenzoIoTIntegration:
    """
    IoT-MCP паттерн: Lorenzo отвечает на вопросы
    о состоянии физической среды.

    "Какова температура в серверной прямо сейчас?"
    → Lorenzo через IoT-MCP считывает датчик
    → Отвечает на основе реальных данных
    """

    async def answer_with_iot_context(self, query: str) -> str:
        # Если запрос о физических показателях → опросить устройства
        if self.is_iot_query(query):
            sensor_data = await self.iot_mcp.read_relevant_sensors(query)
            context = f"Текущие показания: {sensor_data}"
            return await self.llm_qa.ask(query, context=context)
        return await self.llm_qa.ask(query)
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **IoT-MCP + Cognitive Memory (R31)** | Агент помнит историю показаний датчиков → контекстные аномалии |
| **IoT-MCP + AI Routing Lab (R35)** | ML предсказывает отказ оборудования → IoT-MCP превентивно переключает |
| **IoT-MCP + LangGraph (R35)** | LangGraph граф: sensor_read → analysis → actuator_command цикл |
| **IoT-MCP + Meta-Monitor (R29)** | Meta-Monitor видит аномалии в IoT метриках → LLM диагностирует |
| **IoT-MCP + Edge Pi (R34)** | Raspberry Pi = edge IoT-MCP node для локального управления без облака |

## Контакт

- Статья: https://habr.com/ru/articles/953648/ (октябрь 2025)
- GitHub: https://github.com/poly-mcp/IoT-Edge-MCP-Server (MQTT + Modbus + SCADA)
- MCP Protocol: modelcontextprotocol.io
- Смежная (фабричный антивирус, цифровой двойник): https://habr.com/ru/companies/friflex/articles/1014940/
- Смежная (байесовский анализ отказов нефтегаз): https://habr.com/ru/articles/953298/
- Eclipse Mosquitto MQTT: mosquitto.org

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
- [Решения](../../../DECISIONS.md)
