from fastapi import APIRouter, Body, Depends
from typing import Annotated
from sqlalchemy.orm import Session

from ..dependencies.database import get_db
from ..dependencies.application import create_application_pipe
from ..database.models import Application as ApplicationModel, Credentials
from ..schemas.application import Application, ApplicationCreate
from ..utilities.key import generate_api_key

router = APIRouter()


@router.post("", dependencies=[Depends(create_application_pipe)])
def create_application(
    body: ApplicationCreate,
    db: Annotated[Session, Depends(get_db)],
) -> Application:
    application = ApplicationModel(name=body.name.lower(), api_key=generate_api_key())
    db.add(application)
    db.commit()
    db.refresh(application)

    application_credentials = Credentials(
        application_uuid=application.uuid,
        type=1 if body.credentials_type.lower() == "mailgun" else 2,
        values=body.credentials_values,
    )
    db.add(application_credentials)
    db.commit()

    return application
