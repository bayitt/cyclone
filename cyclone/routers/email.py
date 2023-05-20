from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..schemas.email import Email, EmailCreate, EmailUpdate
from ..dependencies.database import get_db
from ..dependencies.email import email_by_name_pipe, email_by_uuid_pipe
from ..database.models import Email as EmailModel

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
    body_dict["template"] = body.template.replace("+#<", "{{")
    body_dict["template"] = body_dict["template"].replace("+#>", "}}")
    email = EmailModel(application_uuid=application_uuid, **body_dict)
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

    if body_dict.get("template"):
        body_dict["template"] = body.template.replace("+#<", "{{")
        body_dict["template"] = body_dict["template"].replace("+#>", "}}")

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
