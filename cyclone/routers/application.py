from fastapi import APIRouter, Body, Depends
from typing import Annotated
from sqlalchemy.orm import Session

from ..dependencies.database import get_db
from ..dependencies.application import create_application_pipe, update_application_pipe
from ..database.models import Application as ApplicationModel, Credentials
from ..schemas.application import Application, ApplicationCreate, ApplicationUpdate
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
        type=body.credentials_type.value,
        values=body.credentials_values,
    )
    db.add(application_credentials)
    db.commit()

    return application


@router.put("/{application_uuid}")
def update_application(
    body: ApplicationUpdate,
    application: ApplicationModel = Depends(update_application_pipe),
    db: Session = Depends(get_db),
) -> Application:
    body_dict = body.dict(exclude_unset=True)

    for key, value in body_dict.items():
        setattr(application, key, value)

    db.commit()
    return application
