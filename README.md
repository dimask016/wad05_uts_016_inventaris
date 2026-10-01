cat > README.md << 'EOF'
# UTS WAD05 — Dashboard Inventaris

**Nama:** Dimas Kurniawan
**NIM:** 25120300016  
**Kelas:** Web Application Development (WAD05)
**Soal:** B — Dashboard Inventaris (NIM Genap)  
**Tema:** Inventaris Part Server Data Center

---

## 📋 Deskripsi

Mini dashboard full-stack untuk mengelola data inventaris part server
data center. Dibangun dengan **Vue 3 (Composition API)** di sisi frontend
dan **FastAPI + Pydantic** di sisi backend, sebagai pemenuhan UTS
mata kuliah Pengembangan Aplikasi Web (WAD05).

### Fitur Utama

- Menampilkan daftar barang inventaris dari backend
- Pencarian berdasarkan **nama** atau **kategori** barang
- Pengurutan **A-Z / Z-A** berdasarkan nama barang
- Badge status stok otomatis: **Aman**, **Menipis**, **Habis**
- Form tambah barang baru (POST ke backend)
- Tombol hapus barang per item (DELETE ke backend)
- 4 tile ringkasan statistik di atas daftar
- Responsif di desktop, tablet, dan mobile
- Dokumentasi API otomatis di `/docs` (Swagger UI)

---

## 🗂 Struktur Folder
uts-wad05/
├── README.md
├── backend-fastapi/
│ ├── main.py # Kode utama FastAPI
│ ├── seed_barang.json # Data awal (20 barang)
│ ├── requirements.txt # Dependensi Python
│ ├── .gitignore
│ └── venv/ # (tidak di-commit)
└── dashboard-vue/
├── index.html
├── package.json
├── vite.config.js
├── public/
│ └── splash.css # CSS splash screen
└── src/
├── main.js
├── style.css
├── App.vue
└── components/
├── RingkasanTiles.vue
├── TambahBarangForm.vue
└── BarangCard.vue

text

---

## 🚀 Cara Menjalankan

### Prasyarat

| Tools | Versi Minimum | Cek dengan |
|-------|---------------|------------|
| Python | 3.10+ | `python3 --version` |
| pip | terbaru | `pip --version` |
| Node.js | 18+ (LTS) | `node --version` |
| npm | 9+ | `npm --version` |

---

### 1️⃣ Menjalankan Backend (FastAPI)

Buka **terminal 1**, lalu:

```bash
cd backend-fastapi

# Buat virtual environment (sekali saja)
python3 -m venv venv

# Aktifkan venv
source venv/bin/activate        # Linux/macOS
# venv\Scripts\activate         # Windows

# Install dependensi
pip install -r requirements.txt

# Jalankan server
uvicorn main:app --reload --host 0.0.0.0 --port 8000

Endpoint yang tersedia:

Method	Endpoint	Deskripsi
GET	/	Cek status backend
GET	/barang	Ambil semua barang (bisa ?q=keyword)
GET	/barang/{id}	Ambil satu barang
POST	/barang	Tambah barang baru
DELETE	/barang/{id}	Hapus barang
PUT	/barang/{id}	Update barang (bonus)
GET	/docs	Swagger UI (dokumentasi otomatis)
