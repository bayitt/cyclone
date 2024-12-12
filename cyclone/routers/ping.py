from fastapi import APIRouter, Depends, status
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from ..dependencies.database import get_db
from ..database.models import Application

router = APIRouter()


@router.post("")
def ping(db: Annotated[Session, Depends(get_db)]):
    try:
        db.query(Application).filter(
            Application.name == "random-application-name"
        ).first()
        return {"database": "healthy"}
    except Exception:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"database": "unhealthy"}
        )
