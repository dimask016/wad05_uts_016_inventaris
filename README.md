# UTS WAD05 — Dashboard Inventaris

Nama: Dimas Kurniawan
NIM: 25120300016 (GENAP — Soal B)

## Cara Menjalankan

### Backend (FastAPI)
```bash
cd backend-fastapi
python -m venv venv
venv\Scripts\activate            # Windows
# source venv/bin/activate       # macOS/Linux
pip install -r requirements.txt
uvicorn main:app --reload
