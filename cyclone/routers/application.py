from fastapi import APIRouter, Body, Depends
from typing import Annotated

from ..database.setup import SessionLocal
from ..dependencies.database import get_db
from ..schemas.application import ApplicationCreate

router = APIRouter()


@router.post()
def create_application(
    body: Annotated[ApplicationCreate, Body()],
    db: Annotated[SessionLocal, Depends(get_db)],
):
    return {"yeahahah": "sjsjsj"}
