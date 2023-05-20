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
    if not authorization or len(authorization.split(" ")) != 2:
        HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Api key is missing",
        )

    api_key = authorization.split(" ")[1]

    application = db.query(Application).filter(Application.api_key == api_key).first()

    if not application:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Application with api key {api_key} does not exist",
        )

    email = (
        db.query(Email)
        .filter(
            Email.application_uuid == application.uuid, Email.name == body.email.upper()
        )
        .first()
    )

    if not email:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Email with name {body.email.upper()} does not exist",
        )

    if not email.variables:
        return email

    request_variables = body.variables or dict()
    missing_variables = list()

    for variable in email.variables:
        if not request_variables.get(variable):
            missing_variables.append(variable)

    if len(missing_variables) > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The following variables are missing - {', '.join(missing_variables)} ",
        )

    return (email, application)
