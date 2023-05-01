from fastapi import APIRouter, Body, Depends
from typing import Annotated
from sqlalchemy.orm import Session

from ..dependencies.database import get_db
from ..dependencies.application import create_application_pipe
from ..database.models import Application, Credentials
from ..schemas.application import Application, ApplicationCreate

router = APIRouter()


@router.post("", dependencies=[Depends(create_application_pipe)])
def create_application(
    body: Annotated[ApplicationCreate, Body()],
    db: Annotated[Session, Depends(get_db)],
) -> Application:
    application = Application(name=body.name)
    db.add(application)
    db.commit()
    db.refresh()

    application_credentials = Credentials(
        application_uuid=application.uuid,
        type=body.credentials_type,
        values=body.credentials_values,
    )
    db.add(application_credentials)
    db.commit()
    db.refresh()

    return application
