from fastapi import APIRouter, Depends
from typing import List
from ..db import get_session
from sqlmodel import Session
router = APIRouter(prefix='/search', tags=['search'])

@router.get('')
def search(q: str = '', limit: int = 5, session: Session = Depends(get_session)):
    # This is a fake search for demo. Replace with vector DB query + mapping.
    fake = [
        {'title': 'Leave Policy', 'snippet': 'Employees are entitled to 12 casual leaves per year...', 'document_id': 'doc-1', 'chunk_id': 'ch-1', 'source': 'HR - PDF'},
        {'title': 'Onboarding Checklist', 'snippet': 'Step 1: Create GitHub account. Step 2: Set up dev environment...', 'document_id': 'doc-2', 'chunk_id': 'ch-2', 'source': 'Notion'}
    ]
    q = (q or '').lower()
    res = [r for r in fake if q in r['title'].lower() or q in r['snippet'].lower()][:limit]
    return {'q': q, 'results': res}
