OrgAI - FastAPI Backend (Demo)
==============================

This is a minimal FastAPI backend scaffold for the OrgAI project. It provides:
- SQLModel-based DB models and a simple DB init script
- Connectors API (create/list/test/sync/delete) with OAuth/token patterns (stubs)
- Document view endpoint that returns a presigned URL for S3-compatible storage (Cloudflare R2-compatible via boto3)
- Simple search stub that returns fake search results (to be replaced with vector DB + LangChain ingestion)
- Job enqueing stub for ingestion/reindex (in-memory queue simulation)

NOTE: This is a demo scaffold. Secrets and production hardening are NOT included.
For demo convenience the app uses SQLite by default. To use Postgres, set DATABASE_URL env var, e.g.:
  export DATABASE_URL="postgresql+psycopg2://user:pass@host:5432/dbname"

To run locally (demo):
  pip install -r requirements.txt
  uvicorn app.main:app --reload --port 8000

Project structure:
  /app
    main.py          - FastAPI app entry
    db.py            - DB engine + init helper
    models.py        - SQLModel models (organizations, users, documents, document_chunks, connectors, logs, recent_queries)
    crud.py          - simple CRUD helpers
    routers/
      connectors.py  - connectors endpoints
      documents.py   - document view endpoint (presign)
      search.py      - search stub
      health.py      - health check
    s3client.py      - S3/R2 presign helper (boto3 wrapper)
  requirements.txt
  .env.example      - environment variable hints

