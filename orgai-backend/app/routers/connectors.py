from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ..db import get_session
from sqlmodel import Session
from ..crud import list_connectors, create_connector, get_connector
router = APIRouter(prefix='/connectors', tags=['connectors'])

# For demo: org_id is fixed; in prod this comes from auth/session
DEMO_ORG = 'demo-org'

@router.get('', response_model=List[dict])
def list_connectors_endpoint(session: Session = Depends(get_session)):
    rows = list_connectors(session, DEMO_ORG)
    return [r.dict(exclude={'config'}) for r in rows]

@router.post('', status_code=201)
def create_connector_endpoint(payload: dict, session: Session = Depends(get_session)):
    # payload: { type, name, config }
    type_ = payload.get('type'); name = payload.get('name') or f'{type_}-auto'
    config = payload.get('config') or {}
    c = create_connector(session, DEMO_ORG, type_, name, config)
    return c.dict(exclude={'config'})

@router.post('/{connector_id}/test')
def test_connector(connector_id: str, session: Session = Depends(get_session)):
    c = get_connector(session, connector_id)
    if not c:
        raise HTTPException(status_code=404, detail='Connector not found')
    # perform a fake test
    c.status = 'connected'
    session.add(c); session.commit(); session.refresh(c)
    return {'ok': True, 'status': c.status}

@router.post('/{connector_id}/sync')
def sync_connector(connector_id: str, session: Session = Depends(get_session)):
    c = get_connector(session, connector_id)
    if not c:
        raise HTTPException(status_code=404, detail='Connector not found')
    # enqueue job or simulate ingestion
    c.status = 'syncing'
    session.add(c); session.commit(); session.refresh(c)
    # For demo: simulate finishing
    c.status = 'idle'
    session.add(c); session.commit(); session.refresh(c)
    return {'ok': True, 'status': c.status}

@router.delete('/{connector_id}')
def delete_connector(connector_id: str, session: Session = Depends(get_session)):
    c = get_connector(session, connector_id)
    if not c:
        raise HTTPException(status_code=404, detail='Connector not found')
    session.delete(c); session.commit()
    return {'ok': True}
