import os
from typing import List
from requests import post, Response


class MailgunException(Exception):
    def __init__(self, message: str):
        self.message = message


class Mailgun:
    FROM_TITLE = "Price Alert"
    FROM_EMAIL = "do_not_reply@sandbox7505f872dead47da97f0bc3c237df941.mailgun.org"

    @classmethod
    def send_mail(cls, email: List[str], subject: str, text: str, html: str) -> Response:
        api_key = os.environ.get("MAILGUN_API_KEY", None)
        domain = os.environ.get("MAILGUN_DOMAIN", None)

        if api_key is None:
            raise MailgunException("There was an error loading the API key")

        if domain is None:
            raise MailgunException("There was an error loading the Domain")

        response = post(f"{domain}/messages",
                        auth=("api", api_key),
                        data={"from": f"{cls.FROM_TITLE} <{cls.FROM_EMAIL}>",
                              "to": email,
                              "subject": subject,
                              "text": text,
                              "html": html})

        if response.status_code != 200:
            raise MailgunException("There was an error sending the email.")

        return response
