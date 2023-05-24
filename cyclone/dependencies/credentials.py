from fastapi import Depends, status
from uuid import UUID
from sqlalchemy.orm import Session
from typing import Annotated

from .database import get_db
from ..database.models import Credentials
from ..schemas.credentials import CredentialsUpdate
from ..utilities.exception import CycloneHTTPException


def credentials_by_uuid_pipe(
    body: CredentialsUpdate,
    credentials_uuid: UUID,
    db: Annotated[Session, Depends(get_db)],
):
    credentials = (
        db.query(Credentials).filter(Credentials.uuid == credentials_uuid).first()
    )

    if not credentials:
        raise CycloneHTTPException(
            error="credentials-001",
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Credentials with uuid {credentials_uuid} does not exist",
        )

    if body.values or body.type:
        type = body.type or credentials.type
        values = body.values or credentials.values

        if type == 1:
            mailgun_keys = ["domain", "api_key", "from_name", "from_address"]
        invalidated_keys = list()

        for key in mailgun_keys:
            if not values.get(key):
                invalidated_keys.append(key)

        if len(invalidated_keys) > 0:
            raise CycloneHTTPException(
                error="credentials-003",
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{', '.join(invalidated_keys)} - missing from values",
            )

    return credentials
