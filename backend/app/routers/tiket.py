from typing import Optional

from fastapi import APIRouter, HTTPException, Query, Response
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/tiket", tags=["tiket"])


class TiketCreate(BaseModel):
    kode_tiket: str = Field(
        ...,
        pattern=r"^EVT-\d{4}$",
        description="Kode tiket dengan pola EVT-XXXX, contoh: EVT-0001",
        examples=["EVT-0001"],
    )
    kuota: int = Field(..., gt=0, description="Kuota tiket, harus lebih dari 0")


class TiketOut(BaseModel):
    id: int
    kode_tiket: str
    kuota: int


db: dict[int, TiketOut] = {}
_next_id: int = 1


@router.post("", response_model=TiketOut, status_code=201)
def create_tiket(payload: TiketCreate, response: Response):
    global _next_id

    tiket = TiketOut(id=_next_id, kode_tiket=payload.kode_tiket, kuota=payload.kuota)
    db[_next_id] = tiket

    response.headers["Location"] = f"/api/tiket/{_next_id}"

    _next_id += 1
    return tiket


@router.get("", response_model=list[TiketOut], status_code=200)
def list_tiket(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    search: Optional[str] = Query(None),
):
    items = list(db.values())

    if search:
        items = [t for t in items if search.lower() in t.kode_tiket.lower()]

    return items[skip : skip + limit]


@router.get("/{tiket_id}", response_model=TiketOut, status_code=200)
def get_tiket(tiket_id: int):
    tiket = db.get(tiket_id)
    if tiket is None:
        raise HTTPException(status_code=404, detail="Tiket tidak ditemukan")
    return tiket