import requests

from ..database.models import Credentials

def send_mailgun_mail(credentials: Credentials):
    print("")
