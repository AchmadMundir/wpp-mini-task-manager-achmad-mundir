# Panduan Pengerjaan dan Menjalankan Project

Dokumen ini ditujukan untuk Achmad Mundir Wicaksono sebagai panduan memahami, mengedit, menjalankan, menguji, dan mempresentasikan source code Mini Task Manager.

## 1. Platform yang digunakan

Gunakan perangkat berikut pada laptop Windows:

1. **Visual Studio Code** sebagai tempat membaca dan mengedit seluruh source code.
2. **Docker Desktop** untuk menjalankan PostgreSQL, backend, dan frontend secara mudah.
3. **Python 3.12** untuk backend FastAPI dan unit test jika ingin menjalankan service secara manual.
4. **Node.js 22 LTS** untuk frontend React jika ingin menjalankan service secara manual.
5. **Git** untuk membuat commit dan mengirim repository ke GitHub.
6. **Postman** bersifat opsional karena API juga dapat diperiksa melalui Swagger di `http://localhost:8000/docs`.

Extension VS Code yang disarankan:

- Python dari Microsoft
- Pylance
- Docker
- ESLint
- GitLens, opsional

## 2. Membuka project di VS Code

1. Ekstrak file ZIP.
2. Buka Visual Studio Code.
3. Pilih **File > Open Folder**.
4. Pilih folder `wpp-task-manager`, bukan hanya `backend` atau `frontend`.
5. Buka terminal VS Code melalui **Terminal > New Terminal**.

Struktur yang akan terlihat:

```text
wpp-task-manager/
├── backend/              FastAPI, PostgreSQL model, migration, dan test
├── frontend/             React, API client, komponen, dan CSS
├── docker-compose.yml    Menjalankan tiga container terpisah
├── README.md             Dokumentasi utama untuk reviewer
└── PANDUAN_PENGERJAAN_ID.md
```

## 3. Cara tercepat menjalankan aplikasi

Pastikan Docker Desktop sudah terbuka dan statusnya **Engine running**. Di terminal VS Code pada folder utama:

```powershell
Copy-Item .env.example .env
docker compose up --build
```

Tunggu sampai log menampilkan bahwa Uvicorn dan Vite telah berjalan. Buka:

- Aplikasi: `http://localhost:5173`
- Swagger API: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/health`

Penggunaan pertama:

1. Masukkan nama board, misalnya `Q3 Website Refresh`.
2. Klik **Add**.
3. Isi judul dan deskripsi task.
4. Klik **Create task**.
5. Ubah status melalui dropdown.
6. Gunakan filter **All**, **To Do**, **In Progress**, atau **Done**.
7. Hapus task atau board untuk menguji endpoint delete.

Untuk berhenti, tekan `Ctrl+C`, lalu jalankan:

```powershell
docker compose down
```

Data tidak hilang karena disimpan dalam volume `postgres_data`. Jangan menjalankan `docker compose down -v` kecuali memang ingin menghapus database lokal.

## 4. Menjalankan backend secara terpisah

Bagian ini membuktikan backend merupakan service independen.

Mulai database dari folder utama:

```powershell
docker compose up -d db
```

Masuk ke backend:

```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
Copy-Item .env.example .env
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```

Jika PowerShell menolak aktivasi virtual environment, jalankan satu kali pada terminal yang sama:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1
```

Uji backend tanpa frontend:

```powershell
curl.exe http://localhost:8000/health
curl.exe http://localhost:8000/api/boards
```

Backend memenuhi requirement jika kedua endpoint menjawab meskipun frontend tidak berjalan.

## 5. Menjalankan frontend secara terpisah

Buka terminal baru di VS Code:

```powershell
cd frontend
Copy-Item .env.example .env
npm install
npm run dev
```

Buka `http://localhost:5173`.

Untuk self-check dari brief, matikan backend tetapi biarkan frontend hidup. Halaman frontend harus tetap muncul dan menampilkan pesan bahwa task service tidak dapat dihubungi. Tampilan tidak boleh putih atau crash.

## 6. Menjalankan pengujian

Masuk ke folder backend dan aktifkan virtual environment:

```powershell
cd backend
.venv\Scripts\Activate.ps1
pytest -v
```

Test reguler tidak memerlukan web server. Hasil yang diharapkan adalah 21 test lulus dan satu integration test dilewati jika `TEST_DATABASE_URL` belum diatur.

Untuk menguji constraint PostgreSQL sebenarnya:

```powershell
$env:TEST_DATABASE_URL="postgresql://task_user:task_password@localhost:5432/task_manager"
pytest -m integration -v
```

Verifikasi build frontend:

```powershell
cd ..\frontend
npm install
npm run build
```

## 7. Urutan membaca source code

Jangan mencoba memahami semua file sekaligus. Gunakan urutan berikut.

### A. Mulai dari database

1. `backend/alembic/versions/0001_create_boards_and_tasks.py`
2. `backend/app/models/board.py`
3. `backend/app/models/task.py`
4. `backend/SCHEMA.md`

Pahami foreign key, `ON DELETE CASCADE`, check constraint, timestamp, dan indeks `(board_id, status)`.

### B. Lanjut ke business logic

1. `backend/app/services/board_service.py`
2. `backend/app/services/task_service.py`
3. `backend/app/core/errors.py`

Service layer memeriksa resource, membersihkan whitespace, memvalidasi status, dan menghasilkan domain error. Service tidak mengetahui detail HTTP.

### C. Pelajari database access

1. `backend/app/repositories/interfaces.py`
2. `backend/app/repositories/sqlalchemy.py`

Interface memungkinkan service diuji dengan fake repository. Implementasi SQLAlchemy melakukan query dan persistence sebenarnya.

### D. Pelajari REST API

1. `backend/app/api/routes/boards.py`
2. `backend/app/api/routes/tasks.py`
3. `backend/app/main.py`
4. `backend/app/core/handlers.py`
5. `backend/API.md`

Route menerjemahkan HTTP request menjadi pemanggilan service. Global handler memastikan semua kegagalan memiliki struktur JSON yang konsisten.

### E. Pelajari unit test

1. `backend/tests/fakes.py`
2. `backend/tests/test_board_service.py`
3. `backend/tests/test_task_service.py`
4. `backend/tests/test_api_errors.py`
5. `backend/tests/test_database_constraints.py`

Perhatikan bahwa test tidak hanya menguji happy path, tetapi juga whitespace, invalid status, dan ID yang tidak tersedia.

### F. Pelajari React

1. `frontend/src/api/client.js`
2. `frontend/src/App.jsx`
3. `frontend/src/components/BoardSidebar.jsx`
4. `frontend/src/components/TaskForm.jsx`
5. `frontend/src/components/TaskList.jsx`
6. `frontend/src/components/TaskCard.jsx`
7. `frontend/src/styles.css`

`client.js` merupakan satu-satunya tempat penyimpanan base URL dan proses normalisasi error. `App.jsx` mengatur state, sedangkan komponen lain berfokus pada tampilan dan interaksi masing-masing.

## 8. Alur request dari awal sampai akhir

Contoh saat pengguna membuat task:

1. Pengguna mengisi `TaskForm`.
2. React memvalidasi agar title tidak kosong.
3. `App.jsx` memanggil `api.createTask()`.
4. Browser mengirim `POST /api/boards/{boardId}/tasks`.
5. FastAPI memvalidasi struktur JSON menggunakan `TaskCreate`.
6. Route memanggil `TaskService.create_task()`.
7. Service memastikan board tersedia dan title bukan whitespace.
8. Repository menyimpan task melalui SQLAlchemy.
9. PostgreSQL memeriksa foreign key, title check, status check, dan tipe data.
10. Backend mengembalikan `201` dengan task baru.
11. React menambahkan task ke state sehingga halaman berubah tanpa reload.

Jika gagal pada tahap mana pun, backend mengirim error konsisten dan frontend menampilkan pesan yang dapat dipahami.

## 9. File yang biasanya Anda edit

| Tujuan perubahan | File utama |
|---|---|
| Mengubah warna dan layout | `frontend/src/styles.css` |
| Mengubah struktur halaman | `frontend/src/App.jsx` |
| Mengubah card task | `frontend/src/components/TaskCard.jsx` |
| Menambah endpoint | `backend/app/api/routes/` |
| Menambah aturan bisnis | `backend/app/services/` |
| Menambah query | `backend/app/repositories/sqlalchemy.py` |
| Mengubah database | model dan migration Alembic baru |
| Menambah test | `backend/tests/` |
| Mengubah URL backend | `frontend/.env` |

Jangan mengubah migration `0001` setelah project dikirim atau digunakan orang lain. Untuk perubahan schema berikutnya, buat migration baru menggunakan:

```powershell
alembic revision --autogenerate -m "describe the change"
alembic upgrade head
```

## 10. Checklist sebelum dikirim

- Jalankan `pytest -v` dan simpan hasilnya.
- Jalankan `npm run build`.
- Jalankan semua service dari clean clone berdasarkan README.
- Pastikan data masih ada setelah backend restart.
- Jalankan backend tanpa frontend dan tes menggunakan `curl.exe`.
- Jalankan frontend tanpa backend dan periksa error state.
- Periksa seluruh endpoint melalui Swagger.
- Pastikan `.env`, `.venv`, `node_modules`, dan `dist` tidak masuk Git.
- Jangan mengklaim fitur yang belum tersedia.

## 11. Mengirim ke GitHub

Dari folder utama:

```powershell
git init
git add .
git commit -m "Complete WPP Media mini task manager assessment"
git branch -M main
git remote add origin URL_REPOSITORY_GITHUB_ANDA
git push -u origin main
```

Jika repository dibuat private, tambahkan reviewer yang disebutkan dalam brief sebagai collaborator. Sebelum mengirim, baca kembali `README.md`, `backend/README.md`, `frontend/README.md`, `API.md`, dan `SCHEMA.md` agar Anda dapat menjelaskan setiap keputusan saat presentasi.

