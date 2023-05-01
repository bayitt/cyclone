from fastapi import Depends, Body, HTTPException, status
from typing import Annotated
from sqlalchemy.orm import Session

from .database import get_db
from ..schemas.application import ApplicationCreate
from ..database.models import Application


def create_application_pipe(
    body: Annotated[ApplicationCreate, Body()], db: Session = Depends(get_db)
):
    application = db.query(Application).filter(Application.name == body.name).first()

    if application:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Application with name {body.name} exists already",
        )
