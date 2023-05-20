from fastapi import Header, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated

from ..database.models import Application, Email
from ..dependencies.database import get_db
from ..schemas.dispatch import DispatchCreate


def dispatch_guard(
    body: DispatchCreate,
    authorization: Annotated[str | None, Header()] = None,
    db: Session = Depends(get_db),
):
    auth_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not authenticated"
    )

    if not authorization or len(authorization.split(" ")) != 2:
        raise auth_exception

    api_key = authorization.split(" ")[1]

    application = db.query(Application).filter(Application.api_key == api_key).first()

    if not application:
        raise auth_exception

    email = (
        db.query(Email)
        .filter(
            Email.application_uuid == application.uuid, Email.name == body.email.upper()
        )
        .first()
    )

    return email
