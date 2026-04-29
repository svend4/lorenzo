# Dockerfile для docs-toolkit
#
# Multi-stage: build → slim runtime.
# Все опциональные зависимости (pypdf, ebooklib, python-docx, anthropic, mcp)
# доступны как extras; в финальном образе ставится `[all]` для удобства.
#
# Использование:
#   docker build -t docs-toolkit .
#
#   # Валидация документов в текущей папке:
#   docker run --rm -v $(pwd):/work -w /work docs-toolkit doc validate
#
#   # Создать документ из шаблона:
#   docker run --rm -v $(pwd):/work -w /work docs-toolkit doc new \
#     --type rfc --slug docs/rfcs/RFC-0001.md
#
#   # Ингестия PDF:
#   docker run --rm -v $(pwd):/work -w /work docs-toolkit ingest report.pdf -o docs/

FROM python:3.11-slim AS builder

WORKDIR /build
COPY pyproject.toml ./
COPY docstoolkit/ ./docstoolkit/

# Build wheel
RUN pip install --no-cache-dir build && \
    python -m build --wheel

FROM python:3.11-slim

LABEL org.opencontainers.image.title="docs-toolkit" \
      org.opencontainers.image.description="Universal markdown documentation toolkit" \
      org.opencontainers.image.source="https://github.com/svend4/lorenzo/tree/main/docs-toolkit" \
      org.opencontainers.image.licenses="MIT"

# Минимальные системные пакеты для опциональных deps
RUN apt-get update && apt-get install -y --no-install-recommends \
        pandoc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY --from=builder /build/dist/*.whl /tmp/

RUN pip install --no-cache-dir /tmp/*.whl[all] && \
    rm -f /tmp/*.whl

# Создать unprivileged пользователя
RUN useradd -m -u 1000 docs
USER docs
WORKDIR /work

ENTRYPOINT ["docstoolkit"]
CMD ["--help"]
