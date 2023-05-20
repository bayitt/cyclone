from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database.models import Dispatch
from ..schemas.dispatch import DispatchCreate
from ..dependencies.database import get_db
from ..dependencies.dispatch import dispatch_guard

router = APIRouter()


@router.post("/send")
def send(body: DispatchCreate):
    print("")
