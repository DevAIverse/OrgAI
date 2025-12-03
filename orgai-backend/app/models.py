from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

# Organizations
class Organization(SQLModel, table=True):
    id: Optional[str] = Field(default=None, primary_key=True)
    name: str
    domain: Optional[str] = None
    metadata: Optional[dict] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)

# Users (very minimal for demo)
class User(SQLModel, table=True):
    id: Optional[str] = Field(default=None, primary_key=True)
    organization_id: Optional[str] = Field(default=None, foreign_key='organization.id')
    email: str
    name: Optional[str] = None
    role: str = 'employee'  # 'employee' | 'admin'
    created_at: datetime = Field(default_factory=datetime.utcnow)

# Connectors
class Connector(SQLModel, table=True):
    id: Optional[str] = Field(default=None, primary_key=True)
    organization_id: Optional[str] = Field(default=None, foreign_key='organization.id')
    type: str   # notion, github, r2, manual
    name: Optional[str] = None
    status: str = 'idle'   # idle | connected | syncing | error
    config: Optional[dict] = Field(default_factory=dict)  # non-secret preview
    created_at: datetime = Field(default_factory=datetime.utcnow)

# Documents
class Document(SQLModel, table=True):
    id: Optional[str] = Field(default=None, primary_key=True)
    organization_id: Optional[str] = Field(default=None, foreign_key='organization.id')
    title: str
    source: Optional[str] = None      # notion, upload, github, pdf
    file_path: Optional[str] = None   # S3 / R2 key
    content_type: Optional[str] = None
    visibility: str = 'all'           # all | admins | self | groups
    uploaded_by: Optional[str] = None
    metadata: Optional[dict] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)

# Document chunks
class DocumentChunk(SQLModel, table=True):
    id: Optional[str] = Field(default=None, primary_key=True)
    document_id: Optional[str] = Field(default=None, foreign_key='document.id')
    organization_id: Optional[str] = Field(default=None, foreign_key='organization.id')
    chunk_index: int = 0
    text: Optional[str] = None
    vector_id: Optional[str] = None
    metadata: Optional[dict] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)

# Search logs & recent queries
class SearchLog(SQLModel, table=True):
    id: Optional[str] = Field(default=None, primary_key=True)
    organization_id: Optional[str] = Field(default=None, foreign_key='organization.id')
    user_id: Optional[str] = Field(default=None, foreign_key='user.id')
    query: str
    result_count: Optional[int] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class RecentQuery(SQLModel, table=True):
    id: Optional[str] = Field(default=None, primary_key=True)
    user_id: Optional[str] = Field(default=None, foreign_key='user.id')
    organization_id: Optional[str] = Field(default=None, foreign_key='organization.id')
    query: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
