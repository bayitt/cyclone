from fastapi import APIRouter

from ..dependencies.database import get_db

router = APIRouter()

@router.post("")
def create_application():
    return {"yeahahah": "sjsjsj"}
