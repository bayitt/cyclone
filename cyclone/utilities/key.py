from random import choices
import string


def generate_api_key():
    return "".join(
        choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=32)
    )
