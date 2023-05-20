from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database.models import Application, Email, Dispatch
from ..schemas.dispatch import DispatchCreate
from ..dependencies.database import get_db
from ..dependencies.dispatch import dispatch_guard

router = APIRouter()


@router.post("/send")
def send(
    body: DispatchCreate,
    dispatch_dependency: tuple[Email, Application] = Depends(dispatch_guard),
    db: Session = Depends(get_db),
):
    email, application = dispatch_dependency
