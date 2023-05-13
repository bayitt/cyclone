from fastapi import Depends, HTTPException, status
from uuid import UUID
from sqlalchemy.orm import Session
from typing import Annotated

from .database import get_db
from ..database.models import Credentials


def credentials_by_uuid_pipe(
    credentials_uuid: UUID, db: Annotated[Session, Depends(get_db)]
):
    credentials = (
        db.query(Credentials).filter(Credentials.uuid == credentials_uuid).first()
    )

    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Credentials with uuid {credentials_uuid} does not exist",
        )

    return credentials
