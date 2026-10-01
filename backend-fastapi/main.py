# ============================================================
# UTS WAD05 — Soal B: Backend Dashboard Inventaris
# FastAPI + Pydantic + CORS
# ============================================================
import json
import os
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# ------------------------------------------------------------
# Inisialisasi aplikasi
# ------------------------------------------------------------
app = FastAPI(
    title="Backend Dashboard Inventaris",
    description=(
        "API untuk mengelola data barang inventaris gudang. "
        "Mendukung GET, POST, DELETE, dan PUT untuk update."
    ),
    version="1.0.0",
)

# ------------------------------------------------------------
# CORS: izinkan frontend Vue (Vite, port 5173)
# ------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://3.24.168.188:3030",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------------------
# Skema Pydantic
# ------------------------------------------------------------
class BarangIn(BaseModel):
    """Skema untuk data barang yang DIKIRIM dari frontend."""
    nama: str = Field(min_length=1, description="Nama barang")
    kategori: str = Field(min_length=1, description="Kategori barang")
    jumlah_stok: int = Field(ge=0, description="Jumlah stok (>= 0)")
    lokasi_gudang: str = Field(min_length=1, description="Lokasi gudang")


class BarangOut(BaseModel):
    """Skema untuk data barang yang DIKEMBALIKAN ke frontend."""
    id: int
    nama: str
    kategori: str
    jumlah_stok: int
    lokasi_gudang: str


class PesanRespons(BaseModel):
    """Skema untuk pesan konfirmasi (DELETE / update)."""
    pesan: str

# ------------------------------------------------------------
# Seed data dari file JSON saat server pertama kali jalan
# ------------------------------------------------------------
SEED_FILE = "seed_barang.json"

if os.path.exists(SEED_FILE):
    with open(SEED_FILE, "r", encoding="utf-8") as f:
        barang_db: list[dict] = json.load(f)
else:
    barang_db: list[dict] = []

# ------------------------------------------------------------
# Endpoint: Root
# ------------------------------------------------------------
@app.get("/", tags=["Root"], summary="Cek status backend")
def baca_root():
    return {"pesan": "Backend Dashboard Inventaris berjalan"}

# ------------------------------------------------------------
# Endpoint: GET /barang — semua barang + filter q (bonus)
# ------------------------------------------------------------
@app.get(
    "/barang",
    response_model=list[BarangOut],
    tags=["Barang"],
    summary="Ambil semua barang",
    description=(
        "Mengembalikan seluruh data barang. Filter opsional q "
        "untuk mencari berdasarkan nama atau kategori."
    ),
)
def baca_semua_barang(q: Optional[str] = None):
    if q:
        kata = q.lower()
        return [
            b for b in barang_db
            if kata in b["nama"].lower()
            or kata in b["kategori"].lower()
        ]
    return barang_db

# ------------------------------------------------------------
# Endpoint: GET /barang/{id}
# ------------------------------------------------------------
@app.get(
    "/barang/{barang_id}",
    response_model=BarangOut,
    tags=["Barang"],
    summary="Ambil satu barang",
)
def baca_satu_barang(barang_id: int):
    for b in barang_db:
        if b["id"] == barang_id:
            return b
    raise HTTPException(status_code=404, detail="Barang tidak ditemukan")

# ------------------------------------------------------------
# Endpoint: POST /barang — tambah barang baru
# ------------------------------------------------------------
@app.post(
    "/barang",
    response_model=BarangOut,
    status_code=201,
    tags=["Barang"],
    summary="Tambah barang baru",
    description="Menerima data barang baru dan mengembalikan data dengan id otomatis.",
)
def tambah_barang(barang: BarangIn):
    id_baru = max((b["id"] for b in barang_db), default=0) + 1
    baru = {"id": id_baru, **barang.model_dump()}
    barang_db.append(baru)
    return baru

# ------------------------------------------------------------
# Endpoint: DELETE /barang/{id}
# ------------------------------------------------------------
@app.delete(
    "/barang/{barang_id}",
    response_model=PesanRespons,
    tags=["Barang"],
    summary="Hapus barang",
    description="Menghapus barang berdasarkan id. Mengembalikan 404 kalau id tidak ada.",
)
def hapus_barang(barang_id: int):
    for i, b in enumerate(barang_db):
        if b["id"] == barang_id:
            dihapus = barang_db.pop(i)
            return {"pesan": f"Barang '{dihapus['nama']}' berhasil dihapus"}
    raise HTTPException(status_code=404, detail="Barang tidak ditemukan")

# ------------------------------------------------------------
# Endpoint BONUS: PUT /barang/{id} — update barang
# ------------------------------------------------------------
@app.put(
    "/barang/{barang_id}",
    response_model=BarangOut,
    tags=["Barang"],
    summary="Update barang",
    description="Mengubah seluruh field barang (nama, kategori, jumlah_stok, lokasi_gudang).",
)
def update_barang(barang_id: int, barang: BarangIn):
    for i, b in enumerate(barang_db):
        if b["id"] == barang_id:
            barang_db[i] = {"id": barang_id, **barang.model_dump()}
            return barang_db[i]
    raise HTTPException(status_code=404, detail="Barang tidak ditemukan")
