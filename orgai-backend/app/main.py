from fastapi import FastAPI
from .db import init_db
from .routers import health, connectors, documents, search

app = FastAPI(title='OrgAI Backend (demo)')

app.include_router(health.router)
app.include_router(connectors.router, prefix='/api')
app.include_router(documents.router, prefix='/api')
app.include_router(search.router, prefix='/api')

@app.on_event('startup')
def on_startup():
    init_db()
