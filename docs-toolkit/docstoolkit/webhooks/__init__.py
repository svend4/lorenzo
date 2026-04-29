"""Webhook dispatcher: events → HTTP endpoints с retry/HMAC/dead-letter.

Использование:
    from docstoolkit.webhooks import WebhookDispatcher, Subscription

    wh = WebhookDispatcher()
    wh.subscribe(Subscription(
        url="https://hooks.example.com/lorenzo",
        events=["job.completed", "feedback.received"],
        secret="hmac-signing-key",
    ))

    # При событии:
    delivery = wh.dispatch(event="job.completed",
                           payload={"job_id": "x", "status": "ok"})
    # delivery: status / attempts / response / error

Подписки и delivery log — в SQLite.
"""
from docstoolkit.webhooks.dispatcher import (
    WebhookDispatcher, Subscription, Delivery, DeliveryStatus,
    sign_payload,
)

__all__ = [
    "WebhookDispatcher", "Subscription", "Delivery", "DeliveryStatus",
    "sign_payload",
]
