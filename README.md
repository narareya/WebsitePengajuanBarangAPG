# Website Pengajuan Barang APG

Aplikasi web untuk pengelolaan pengajuan pembelian barang internal PT APG. Proyek ini dikerjakan sebagai **Technical Assessment Seleksi PKL Amazink Group Indonesia**.

Aplikasi terdiri dari backend **BEAmazink** (FastAPI) dan frontend **FEAmazink** (Vue 3), yang memungkinkan karyawan mengajukan permintaan pembelian barang, atasan (manager/admin) melakukan approval, serta admin mengelola master data user, departemen, dan produk.

🔗 Demo: [website-pengajuan-barang-apg.vercel.app](https://website-pengajuan-barang-apg.vercel.app)

## Daftar Isi

- [Fitur](#fitur)
- [Tech Stack](#tech-stack)
- [Struktur Proyek](#struktur-proyek)
- [Arsitektur Backend](#arsitektur-backend)
- [Skema Data](#skema-data)
- [Instalasi & Menjalankan Proyek](#instalasi--menjalankan-proyek)
  - [Backend](#backend)
  - [Frontend](#frontend)
- [Akun Default (Seeder)](#akun-default-seeder)
- [Dokumentasi API](#dokumentasi-api)

## Fitur

- **Autentikasi & Otorisasi** — Login berbasis JWT dengan role-based access control (`admin`, `manager`, `employee`) dan mekanisme token blacklist untuk logout.
- **Manajemen Pengajuan Barang** — Karyawan dapat membuat pengajuan (request) dengan banyak item produk sekaligus, melihat riwayat pengajuan pribadi, serta mengedit/menghapus pengajuan.
- **Approval Pengajuan** — Manager/admin dapat melihat seluruh pengajuan (dengan filter status & pencarian, serta pagination) dan melakukan approve/reject.
- **Manajemen Produk** — CRUD data produk beserta status aktif/nonaktif.
- **Manajemen Departemen** — CRUD data departemen perusahaan.
- **Manajemen User** — CRUD data user dan penetapan role.
- **Dashboard Ringkasan** — Statistik pengajuan (total, pending, approved, rejected), tren bulanan, dan aktivitas terbaru — tersaring otomatis berdasarkan role yang login.
- **Activity Log** — Pencatatan aktivitas penting di sistem, dapat difilter dan dicari (khusus admin).

## Tech Stack

**Backend (BEAmazink)**
- [FastAPI](https://fastapi.tiangolo.com/) — web framework
- [SQLAlchemy](https://www.sqlalchemy.org/) — ORM
- [Alembic](https://alembic.sqlalchemy.org/) — database migration
- PostgreSQL (via `psycopg2-binary`)
- `python-jose` — JSON Web Token (JWT)
- `passlib` + `bcrypt` — hashing password
- `pydantic` — validasi data/schema
- `uvicorn` — ASGI server

**Frontend (FEAmazink)**
- [Vue 3](https://vuejs.org/) (Composition API)
- [Vite](https://vitejs.dev/) — build tool
- [Vue Router](https://router.vuejs.org/)
- [Pinia](https://pinia.vuejs.org/) — state management
- [Axios](https://axios-http.com/) — HTTP client
- [Tailwind CSS](https://tailwindcss.com/)
- [Lucide Icons](https://lucide.dev/)
- [Vitest](https://vitest.dev/) + Vue Test Utils — unit testing

## Struktur Proyek

```
WebsitePengajuanBarangAPG/
├── backend/                     # BEAmazink - REST API (FastAPI)
│   ├── app/
│   │   ├── config/               # Konfigurasi database (SQLAlchemy engine & session)
│   │   ├── middlewares/          # Auth middleware (JWT & role guard)
│   │   ├── models/                # Model SQLAlchemy (User, Request, Product, dst.)
│   │   ├── repositories/          # Layer akses data (query database)
│   │   ├── schemas/               # Skema Pydantic (request/response)
│   │   ├── services/               # Business logic
│   │   ├── routes/                 # Endpoint/router FastAPI
│   │   ├── utils/                   # Helper (hashing password, dll.)
│   │   └── main.py                  # Entry point aplikasi FastAPI
│   ├── database/
│   │   ├── migrations/              # Migrasi Alembic
│   │   └── seeders/seed.py          # Seeder data awal
│   ├── alembic.ini
│   ├── requirements.txt
│   └── .env.example
│
└── frontend/                     # FEAmazink - SPA (Vue 3)
    └── src/
        ├── api/                    # Wrapper Axios per modul (user, product, request, dst.)
        ├── components/             # Komponen UI per fitur (login, dashboard, request, dll.)
        ├── config/                  # Konfigurasi frontend
        ├── pages/                   # Halaman (Login, Dashboard, User, Product, Request, dst.)
        ├── router/                  # Definisi routing & route guard
        └── stores/                  # Pinia store
```

Backend mengikuti pola **layered architecture**: `routes → services → repositories → models`, dengan validasi input/output melalui `schemas` (Pydantic).

## Arsitektur Backend

Modul-modul utama yang tersedia di backend:

| Modul | Endpoint Prefix | Keterangan |
|---|---|---|
| Auth | `/auth` | Login (`POST /auth/login`) & logout (`POST /auth/logout`) |
| Users | `/users` | CRUD user |
| Departements | `/departements` | CRUD departemen |
| Products | `/products` | CRUD produk (termasuk `GET /products/active`) |
| Requests | `/requests` | Buat, lihat (semua/milik sendiri), approve, update, hapus pengajuan |
| Request Details | `/request-details` | Detail item dalam sebuah pengajuan |
| Dashboard | `/dashboard` | Ringkasan statistik (`GET /dashboard/summary`) |
| Activity Logs | `/activity-logs` | Riwayat aktivitas (khusus admin) |

Autentikasi menggunakan **OAuth2 Password Bearer** dengan JWT. Endpoint yang butuh proteksi menggunakan dependency `get_current_user` (wajib login) atau `require_role(...)` (wajib login + role tertentu, misalnya `require_role("manager", "admin")`).

## Skema Data

Entitas utama pada database (lihat `backend/app/models/`):

- **User** — `user_id`, `name`, `email`, `password` (hashed), `role` (`admin` / `manager` / `employee`), `departement_id`, `user_status`
- **Departement** — `departement_id`, `departement_code`, `departement_name`, `departement_status`
- **Product** — `product_id`, `product_code`, `product_name`, `product_desc`, `product_price`, `product_status`
- **RequestModel** (`requests`) — `request_id`, `user_id`, `request_date`, `status` (`pending` / `approved` / `rejected`), `approved_by`, `approved_at`
- **RequestDetail** (`request_details`) — `detail_id`, `request_id`, `product_id`, `quantity`
- **ActivityLog** (`activity_logs`) — `log_id`, `user_id`, `action`, `entity`, `entity_id`, `description`, `created_at`
- **TokenBlacklist** — menyimpan token JWT yang sudah di-*logout* agar tidak bisa dipakai ulang

## Instalasi & Menjalankan Proyek

### Backend

**Prasyarat:** Python 3.11+ dan PostgreSQL.

1. Masuk ke folder backend dan buat virtual environment:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Salin `.env.example` menjadi `.env`, lalu sesuaikan nilainya:
   ```env
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=
   DB_USER=
   DB_PASSWORD=
   JWT_SECRET_KEY=
   JWT_ALGORITHM=HS256
   JWT_EXPIRE_MINUTES=60
   ```

4. Jalankan migrasi database dengan Alembic:
   ```bash
   alembic upgrade head
   ```

5. (Opsional) Jalankan seeder untuk mengisi data awal (departemen & user contoh):
   ```bash
   python database/seeders/seed.py
   ```

6. Jalankan server pengembangan:
   ```bash
   uvicorn app.main:app --reload
   ```
   API akan berjalan di `http://localhost:8000`.

### Frontend

**Prasyarat:** Node.js `^22.18.0` atau `>=24.12.0`.

1. Masuk ke folder frontend dan install dependencies:
   ```bash
   cd frontend
   npm install
   ```

2. Jalankan server pengembangan:
   ```bash
   npm run dev
   ```
   Aplikasi akan berjalan di `http://localhost:5173` (secara default backend mengizinkan origin ini melalui CORS).

3. Perintah lain yang tersedia:
   ```bash
   npm run build       # build untuk produksi
   npm run preview     # preview hasil build
   npm run test:unit   # menjalankan unit test (Vitest)
   npm run lint        # linting (oxlint + eslint)
   npm run format      # format kode dengan Prettier
   ```

## Akun Default (Seeder)

Setelah menjalankan `seed.py`, tersedia akun berikut untuk mencoba aplikasi:

| Role | Email | Password |
|---|---|---|
| Admin | `admin@apg.com` | `admin123` |
| Manager | `budi@apg.com` | `budi123` |
| Employee | `siti@apg.com` | `siti123` |

> ⚠️ Akun ini hanya untuk kebutuhan development/demo. Ganti kredensial sebelum digunakan di lingkungan produksi.

## Dokumentasi API

Setelah backend berjalan, dokumentasi interaktif (Swagger UI) tersedia otomatis di:

```
http://localhost:8000/docs
```

---

Dibuat sebagai bagian dari Technical Assessment Seleksi PKL **Amazink Group Indonesia**.
