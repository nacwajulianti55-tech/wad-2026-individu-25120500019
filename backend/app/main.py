from fastapi import FastAPI

from app.routers import tiket

app = FastAPI(title="The Build API — Tiket")

app.include_router(tiket.router)


@app.get("/health")
def health():
    """Dicek oleh verify.py — wajib 200 + {"status": "ok"}."""
    return {"status": "ok"}