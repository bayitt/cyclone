from fastapi import APIRouter

router = APIRouter()

@router.post('/send')
def send():
    print("")