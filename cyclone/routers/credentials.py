from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session

from ..dependencies.database import get_db
from ..dependencies.credentials import credentials_by_uuid_pipe
from ..database.models import Credentials as CredentialsModel
from ..schemas.credentials import Credentials, CredentialsUpdate

router = APIRouter()


@router.put("/{credentials_uuid}")
def update_credentials(
    body: CredentialsUpdate,
    credentials: CredentialsModel = Depends(credentials_by_uuid_pipe),
    db: Session = Depends(get_db),
) -> Credentials:
    body_dict = body.dict(exclude_unset=True)

    for key, value in body_dict.items():
        setattr(credentials, key, value)

    db.commit()

    return credentials
