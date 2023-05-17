from fastapi import Header, status, HTTPException
from typing import Annotated

from ..database.models import Application

def dispatch_guard(authorization: Annotated[str | None, Header()] = None):
    print("")