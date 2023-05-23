from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..schemas.email import Email, EmailCreate, EmailUpdate
from ..dependencies.database import get_db
from ..dependencies.email import email_by_name_pipe, email_by_uuid_pipe
from ..database.models import Email as EmailModel
from ..utilities.jinja import parse_incoming_template

router = APIRouter()


@router.post(
    "", status_code=status.HTTP_201_CREATED, dependencies=[Depends(email_by_name_pipe)]
)
def create_email(
    body: EmailCreate,
    application_uuid: str,
    db: Session = Depends(get_db),
) -> Email:
    body_dict = body.dict(exclude_unset=True)
    body_dict["name"] = body.name.upper()
    del body_dict["template"]
    email = EmailModel(
        application_uuid=application_uuid,
        **body_dict,
        _template=parse_incoming_template(body.template)
    )
    db.add(email)
    db.commit()
    db.refresh(email)

    return email


@router.put("/{email_uuid}")
def update_email(
    body: EmailUpdate,
    email: EmailModel = Depends(email_by_uuid_pipe),
    db: Session = Depends(get_db),
) -> Email:
    body_dict = body.dict(exclude_unset=True)

    if body_dict.get("name"):
        body_dict["name"] = body_dict["name"].upper()

    for key, value in body_dict.items():
        setattr(email, key, value)

    db.commit()

    return email


@router.delete("/{email_uuid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_email(
    email: EmailModel = Depends(email_by_uuid_pipe), db: Session = Depends(get_db)
):
    db.delete(email)
    db.commit()
