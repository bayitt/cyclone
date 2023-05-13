from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from typing import Annotated

from ..dependencies.database import get_db
from ..dependencies.credentials import credentials_by_uuid_pipe
from ..database.models import Credentials
from ..schemas.credentials import CredentialsUpdate

router = APIRouter()


@router.put("/{credentials_uuid}")
def update_credentials(
    body: CredentialsUpdate,
    credentials: Credentials = Depends(credentials_by_uuid_pipe),
    db: Session = Depends(get_db),
):
    body_dict = body.dict(exclude_unset=True)

    for key, value in body_dict.items():
        setattr(credentials, key, value)

    db.session.commit()

    return credentials
