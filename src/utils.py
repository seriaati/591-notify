import requests


def line_notify(message: str, *, token: str) -> None:
    requests.post(
        "https://notify-api.line.me/api/notify",
        headers={"Authorization": f"Bearer {token}"},
        data={"message": message},
    )
