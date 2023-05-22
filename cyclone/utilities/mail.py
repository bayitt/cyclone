import requests


def send_mailgun_mail(
    recipients: list[str], subject: str, html: str, config: dict[str, str]
):
    response = requests.post(
        f"https://api.mailgun.net/v3/{config.get('domain')}/messages",
        auth=("api", f"{config.get('api_key')}"),
        data={
            "from": f"{config.get('from_name')} <{config.get('from_address')}>",
            "to": recipients,
            "subject": subject,
            "html": html,
        },
    )

    if response.status_code != 200:
        raise Exception(response.content)
