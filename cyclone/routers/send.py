from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session
from jinja2 import Template
from markupsafe import Markup
import sys

from ..database.models import Application, Email, Credentials, Dispatch
from ..schemas.dispatch import DispatchCreate
from ..dependencies.database import get_db
from ..dependencies.dispatch import dispatch_guard
from ..utilities.jinja import (
    verify_template_directory,
    verify_template_layout,
    get_jinja_env_object,
)
from ..utilities.mail import send_mailgun_mail

router = APIRouter()


@router.post("/send", status_code=status.HTTP_200_OK)
def send(
    body: DispatchCreate,
    response: Response,
    dispatch_dependency: tuple[Email, Application] = Depends(dispatch_guard),
    db: Session = Depends(get_db),
):
    verify_template_directory()
    env = get_jinja_env_object()
    email, application = dispatch_dependency
    verify_template_layout(application)

    template = env.get_template(f"{application.name.lower()}.html")
    html = template.render(
        template=Markup(Template(email.template).render(**body.variables))
    )

    dispatch_data = {
        "application_uuid": application.uuid,
        "email_uuid": email.uuid,
        "template": html,
        "variables": body.variables,
    }
    credentials: Credentials = application.credentials
    logs = None

    try:
        match credentials.type:
            case 1:
                send_mailgun_mail(
                    body.recipients, email.subject, html, credentials.values
                )
            case _:
                send_mailgun_mail(
                    body.recipients, email.subject, html, credentials.values
                )
    except Exception:
        exception = sys.exc_info()
        logs = exception[1]
        dispatch_data["logs"] = str(logs)
        response.status_code = status.HTTP_502_BAD_GATEWAY

    dispatch = Dispatch(**dispatch_data)
    db.add(dispatch)
    db.commit()

    return {
        "message": "The email request failed"
        if logs
        else "The email was sent successfully"
    }
