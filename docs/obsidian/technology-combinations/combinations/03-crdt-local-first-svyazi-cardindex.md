---
title: "Комбинация 3: CRDT local-first × Svyazi CardIndex"
tags:
  - technology-combinations
date: 2026-04-29
---

# Комбинация 3: CRDT local-first × Svyazi CardIndex

<!-- summary -->
> > Источник: MHTML‑снимок `Комбинирование технологий для новых свойств - Claude` (корень репозитория).
**Проекты:** Svyazi, CardIndex, Yjs

---
<!-- tags: knowledge, ingestion, local-first, collaboration -->




> Источник: MHTML‑снимок `Комбинирование технологий для новых свойств - Claude` (корень репозитория).

Родители:

CRDT / RON / Yjs (habr.com/ru/articles/534510/, habr.com/ru/articles/946722/) — conflict-free replicated data types, p2p синхронизация

Svyazi CardIndex — YAML-структура профилей с хешами для дедупликации

Дети:

3.1 P2P-граф сообщества без центрального сервера

Сейчас Svyazi — single-user система. С CRDT:

Каждый участник ведёт локальный CardIndex

Изменения синхронизируются p2p через Yjs

Конфликты (два человека обновили профиль одного участника) мержатся автоматически

Никакого центрального сервера — privacy by design

Для legal-community Max'а: каждый юрист в сообществе ведёт свой локальный граф дел и участников, но всё синхронизируется peer-to-peer. Данные не покидают машины участников.

3.2 Offline-first discovery

Discovery-файл Svyazi (накопление неизвестного) синхронизируется через CRDT между устройствами:

Ноутбук нашёл новую сущность → добавил в discovery

Телефон оффлайн 2 дня

При подключении автоматически получает обновления

Модерация тоже распределённая

<!-- see-also -->

---

**Смотрите также:**
- [[03-local-first]]
- [[01-pravilnaya-agentskaya-arkhitektura-svyazi-pattern]]
- [[11-hybrid-crdt-sql-database]]
- [[20-hybrid-olap-oltp-with-real-time-sync]]


<!-- similar-docs -->

---

**Похожие документы:**
- [[03-local-first]] (сходство 0.44)
- [[03-local-first]] (сходство 0.41)
- [[11-hybrid-crdt-sql-database]] (сходство 0.21)

