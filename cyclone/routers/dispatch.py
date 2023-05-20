from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from jinja2 import Template

from ..database.models import Application, Email, Dispatch
from ..schemas.dispatch import DispatchCreate
from ..dependencies.database import get_db
from ..dependencies.dispatch import dispatch_guard
from ..utilities.jinja import (
    verify_template_directory,
    verify_template_layout,
    get_jinja_env_object,
)

router = APIRouter()


@router.post("/send")
def send(
    body: DispatchCreate,
    dispatch_dependency: tuple[Email, Application] = Depends(dispatch_guard),
    db: Session = Depends(get_db),
):
    verify_template_directory()
    env = get_jinja_env_object()
    email, application = dispatch_dependency
    verify_template_layout(application)

    template = env.get_template(f"{application.name.lower()}.html")
    html = template.render(template=Template(email.template).render(**body.variables))

    print(html)
