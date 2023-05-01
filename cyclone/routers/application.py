from fastapi import APIRouter, Body, Depends
from typing import Annotated
from sqlalchemy.orm import Session

from ..dependencies.database import get_db
from ..dependencies.application import create_application_pipe
from ..schemas.application import ApplicationCreate

router = APIRouter()


@router.post("", dependencies=[Depends(create_application_pipe)])
def create_application(
    body: Annotated[ApplicationCreate, Body()],
    db: Annotated[Session, Depends(get_db)],
):
    return {"yeahahah": "sjsjsj"}
