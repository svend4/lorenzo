---
title: "Пара 3 — CRDT-синхронизация × Self-hosted persistence"
tags:
  - habr-unique-projects
date: 2026-04-29
---

# Пара 3 — CRDT-синхронизация × Self-hosted persistence

<!-- summary -->
> > Источник: MHTML‑снимок `Поиск уникальных проектов на Хабре для совместной разработки - Claude` (корень репозитория).
**Проекты:** Svyazi, CardIndex, Yodoca, Yjs, Automerge

---
<!-- tags: memory, knowledge, ingestion, local-first, architecture, collaboration -->




> Источник: MHTML‑снимок `Поиск уникальных проектов на Хабре для совместной разработки - Claude` (корень репозитория).

Пара 3. CRDT-синхронизация (Yjs/Automerge) × Self-hosted persistence

Родители: Yjs (CRDT-фреймворк, p2p, IndexedDB-персистентность, провайдеры под WebRTC, WebSocket, ElectricSQL, AT Protocol — github.com/yjs/yjs) и Automerge (CRDT с богатой моделью документов, automerge.org). Поодиночке: библиотеки. Eidetica (jackson.dev/post/crdts_as_database) делает их субстратом для разнообразных CRDT, ElectricSQL даёт sync поверх SQLite/Postgres. По отдельности слабые. Вместе — фундамент для multi-device приватной экосистемы без облака.

Дети:

Multi-device vault без подписок — Obsidian-vault на телефоне, ноуте и домашнем сервере синкается через Yjs+IndexedDB без участия Obsidian Sync ($5/mo). Никакого vendor lock-in, никаких proprietary протоколов. Особенно ценно для legal data — она никогда не покидает машины пользователя.

End-to-end encrypted CRDT relay для сообщества — паттерн от kerkour.com (CRDT + e2e encryption): несколько участников твоего сообщества синхронизируют общий vault через минимальный relay-сервер, который видит только зашифрованные дельты. Это техническая реализация того, что Чуян делает руками с CardIndex для участников Svyazi — но peer-to-peer и без необходимости Чуяну быть central authority.

Hierarchical CRDT memory layers — рабочий контекст (быстрый CRDT), эпизодический (среднее окно), семантический (медленный, append-only) живут как разные CRDT-документы поверх одного sync engine. Это синхронизируемая многоуровневая память Yodoca/xMemory, которая «следует» за тобой между устройствами.

<!-- see-also -->

---

**Смотрите также:**
- [[4-riscv-privacy]]
- [[03-crdt-local-first-svyazi-cardindex]]
- [[3-zinc-hybrid-arch]]
- [[6-metaphor]]


<!-- similar-docs -->

---

**Похожие документы:**
- [[4-riscv-privacy]] (сходство 0.21)
- [[3-zinc-hybrid-arch]] (сходство 0.19)
- [[03-crdt-local-first-svyazi-cardindex]] (сходство 0.18)

