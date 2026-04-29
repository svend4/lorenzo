"""OpenTelemetry tracer wrapper. Работает без OTel — fallback на stub."""
import time
from contextlib import contextmanager
from dataclasses import dataclass, field


@dataclass
class Span:
    """Один span (для stub)."""
    name: str
    started_ns: int = 0
    ended_ns: int = 0
    attributes: dict = field(default_factory=dict)
    status: str = "ok"           # ok | error
    events: list[dict] = field(default_factory=list)

    @property
    def duration_ms(self) -> float:
        if self.ended_ns and self.started_ns:
            return (self.ended_ns - self.started_ns) / 1_000_000
        return 0.0

    def set_attribute(self, key: str, value):
        self.attributes[key] = value

    def add_event(self, name: str, attributes: dict | None = None):
        self.events.append({
            "name": name, "attributes": attributes or {},
            "ts_ns": time.time_ns(),
        })

    def record_exception(self, exc: Exception):
        self.status = "error"
        self.add_event("exception", {
            "type": type(exc).__name__,
            "message": str(exc)[:500],
        })


class StubTracer:
    """No-op tracer + локальный буфер последних spans для дебага."""

    def __init__(self, max_buffer: int = 100):
        self.spans: list[Span] = []
        self.max_buffer = max_buffer

    @contextmanager
    def span(self, name: str, attributes: dict | None = None):
        s = Span(name=name, started_ns=time.time_ns(),
                 attributes=attributes or {})
        try:
            yield s
        except Exception as e:
            s.record_exception(e)
            raise
        finally:
            s.ended_ns = time.time_ns()
            self.spans.append(s)
            if len(self.spans) > self.max_buffer:
                self.spans = self.spans[-self.max_buffer:]

    def get_recent(self, n: int = 20) -> list[Span]:
        return self.spans[-n:]


class OTelTracer:
    """Adapter к настоящему OpenTelemetry tracer."""

    def __init__(self, otel_tracer):
        self._otel = otel_tracer

    @contextmanager
    def span(self, name: str, attributes: dict | None = None):
        with self._otel.start_as_current_span(name, attributes=attributes or {}) as otel_span:
            wrapper = _OTelSpanWrapper(otel_span)
            try:
                yield wrapper
            except Exception as e:
                wrapper.record_exception(e)
                raise


class _OTelSpanWrapper:
    """Перенаправляет вызовы Span API на otel span."""

    def __init__(self, otel_span):
        self._otel = otel_span

    def set_attribute(self, key, value):
        self._otel.set_attribute(key, value)

    def add_event(self, name, attributes=None):
        self._otel.add_event(name, attributes=attributes or {})

    def record_exception(self, exc):
        self._otel.record_exception(exc)


# Module-level
_default_tracer: StubTracer | OTelTracer = StubTracer()


def get_tracer():
    return _default_tracer


def init_telemetry(otlp_endpoint: str = "",
                    service_name: str = "docs-toolkit",
                    enable_console: bool = False):
    """Инициализация OpenTelemetry, если SDK установлен.

    Если otlp_endpoint пуст и enable_console=False — остаётся stub tracer.
    """
    global _default_tracer
    try:
        from opentelemetry import trace
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import (
            BatchSpanProcessor, ConsoleSpanExporter,
        )
        from opentelemetry.sdk.resources import Resource
    except ImportError:
        return False  # OTel SDK не установлен — fallback на stub

    resource = Resource.create({"service.name": service_name})
    provider = TracerProvider(resource=resource)

    if enable_console:
        provider.add_span_processor(
            BatchSpanProcessor(ConsoleSpanExporter())
        )

    if otlp_endpoint:
        try:
            from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
            provider.add_span_processor(
                BatchSpanProcessor(OTLPSpanExporter(endpoint=otlp_endpoint))
            )
        except ImportError:
            pass  # OTLP exporter не установлен

    trace.set_tracer_provider(provider)
    otel_tracer = trace.get_tracer(service_name)
    _default_tracer = OTelTracer(otel_tracer)
    return True


# Convenience: tracer.span("name")
class _TracerProxy:
    @contextmanager
    def span(self, name: str, attributes: dict | None = None):
        with _default_tracer.span(name, attributes) as s:
            yield s


tracer = _TracerProxy()
