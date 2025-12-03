from fastapi import APIRouter, Depends, HTTPException
from ..db import get_session
from sqlmodel import Session
from ..models import Document, DocumentChunk
from ..s3client import presign_get
router = APIRouter(prefix='/documents', tags=['documents'])

DEMO_ORG = 'demo-org'

@router.get('/{document_id}/view')
def view_document(document_id: str, chunk_id: str = None, session: Session = Depends(get_session)):
    # fetch document and chunk metadata
    doc = session.get(Document, document_id)
    if not doc:
        raise HTTPException(status_code=404, detail='Document not found')
    # demo: simple permission pass; in prod implement ACL here
    signed_url = None
    if doc.file_path:
        signed_url = presign_get(doc.file_path, expires_in=300)
    chunk_meta = {}
    if chunk_id:
        chunk = session.get(DocumentChunk, chunk_id)
        if chunk and chunk.document_id == document_id:
            chunk_meta = chunk.metadata or {}
            chunk_meta['snippet'] = (chunk.text or '')[:300]
    return {
        'signed_url': signed_url,
        'content_type': doc.content_type,
        'title': doc.title,
        'chunk_meta': chunk_meta
    }
