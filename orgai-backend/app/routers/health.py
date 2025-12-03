from fastapi import APIRouter
from ..db import init_db
router = APIRouter(prefix='/health')

@router.get('/ready')
def ready():
    # ensure DB can be initialised
    init_db()
    return {'status': 'ok'}
