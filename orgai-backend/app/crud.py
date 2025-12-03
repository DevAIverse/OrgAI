from sqlmodel import select
from .models import Connector, Document, DocumentChunk, SearchLog, RecentQuery
from ..app.db import get_session
from typing import List
from sqlmodel import Session

def list_connectors(session: Session, org_id: str):
    return session.exec(select(Connector).where(Connector.organization_id == org_id)).all()

def create_connector(session: Session, org_id: str, type_: str, name: str, config: dict):
    c = Connector(organization_id=org_id, type=type_, name=name, config=config, status='connected')
    session.add(c); session.commit(); session.refresh(c)
    return c

def get_connector(session: Session, connector_id: str):
    return session.get(Connector, connector_id)

def create_document(session: Session, org_id: str, title: str, source: str, file_path: str, content_type: str, visibility: str, uploaded_by: str, metadata: dict):
    d = Document(organization_id=org_id, title=title, source=source, file_path=file_path, content_type=content_type, visibility=visibility, uploaded_by=uploaded_by, metadata=metadata)
    session.add(d); session.commit(); session.refresh(d)
    return d

def create_chunk(session: Session, document_id: str, org_id: str, idx: int, text: str, metadata: dict):
    c = DocumentChunk(document_id=document_id, organization_id=org_id, chunk_index=idx, text=text, metadata=metadata)
    session.add(c); session.commit(); session.refresh(c)
    return c
