from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..schemas.email import Email, EmailCreate
from ..dependencies.database import get_db
from ..dependencies.email import email_by_name_pipe
from ..database.models import Email as EmailModel

router = APIRouter()


@router.post("", dependencies=[Depends(email_by_name_pipe)])
def create_email(
    body: EmailCreate,
    application_uuid: str,
    db: Session = Depends(get_db),
) -> Email:
    body_dict = body.dict(exclude_unset=True)
    body_dict["name"] = body.name.upper()
    email = EmailModel(application_uuid=application_uuid, **body_dict)
    db.add(email)
    db.commit()
    db.refresh(email)

    return email
