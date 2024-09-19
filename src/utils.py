from __future__ import annotations

import requests

__all__ = ("line_notify",)


def line_notify(token: str, *, message: str) -> None:
    requests.post(
        "https://notify-api.line.me/api/notify",
        headers={"Authorization": f"Bearer {token}"},
        data={"message": message},
        timeout=10,
    )
