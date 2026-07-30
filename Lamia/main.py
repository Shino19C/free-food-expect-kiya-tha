import asyncio
from contextlib import suppress
from pathlib import Path

from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

try:
    from .database import Base, engine, SessionLocal
    from .models import SOSReport
    from .schemas import SOSCreate
    from . import crud
except ImportError:
    from database import Base, engine, SessionLocal
    from models import SOSReport
    from schemas import SOSCreate
    import crud

Base.metadata.create_all(bind=engine)


async def cleanup_loop():
    while True:
        await asyncio.sleep(3600)
        db = SessionLocal()
        try:
            crud.cleanup_expired_sos(db)
        finally:
            db.close()


app = FastAPI(title="SOS Backend")
BASE_DIR = Path(__file__).resolve().parent


@app.on_event("startup")
def startup_event():
    asyncio.create_task(cleanup_loop())


@app.get("/", response_class=HTMLResponse)
def root():
    index_page = BASE_DIR / "templates" / "index.html"
    return index_page.read_text(encoding="utf-8")


@app.get("/health")
def health():
    return {"status": "ok"}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/sos")
def create_sos(report: SOSCreate,
               db: Session = Depends(get_db)):
    return crud.create_sos(db, report)


@app.get("/sos")
def get_sos(db: Session = Depends(get_db)):
    return crud.get_all_sos(db)


@app.patch("/sos/{report_id}")
def resolve(report_id: int,
            db: Session = Depends(get_db)):

    report = crud.resolve_sos(db, report_id)

    if report is None:
        raise HTTPException(
            status_code=404,
            detail="SOS not found"
        )

    return report


if __name__ == "__main__":
    import os
    import uvicorn

    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    cert_file = os.getenv("SSL_CERTFILE", "/home/shino/genesis/free-food-expect-kiya-tha/Lamia/certs/cert.pem")
    key_file = os.getenv("SSL_KEYFILE", "/home/shino/genesis/free-food-expect-kiya-tha/Lamia/certs/key.pem")

    ssl_config = {}
    if os.path.exists(cert_file) and os.path.exists(key_file):
        ssl_config = {"ssl_certfile": cert_file, "ssl_keyfile": key_file}

    uvicorn.run(app, host=host, port=port, **ssl_config)