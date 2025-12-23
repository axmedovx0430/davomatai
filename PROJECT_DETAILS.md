# DavomatAI: Technical Project Details

## 1. Project Purpose and Overall Idea
**DavomatAI** is an automated attendance system that uses face recognition to track employee/student attendance. 
- **Core Workflow**: An ESP32-CAM captures images and sends them to a FastAPI backend. The backend uses the InsightFace library to detect and recognize faces. If a match is found, attendance is recorded in a PostgreSQL database, and a real-time notification is sent via a Telegram Bot.
- **Management**: A Next.js admin panel allows administrators to manage users, groups, schedules, and view attendance statistics.
- **Mobile Access**: A Telegram Mini App and a Flutter mobile app provide users with access to their own attendance history and stats.

## 2. Backend Technology
- **Language**: Python 3.11
- **Framework**: FastAPI (0.104.1)
- **Database ORM**: SQLAlchemy (2.0.23)
- **Database Driver**: psycopg2-binary (PostgreSQL)
- **Face Recognition**: InsightFace (0.7.3) with ONNXRuntime (1.17.0)
- **Model**: `buffalo_s` (Small/Lite version for memory efficiency)
- **Other**: `python-telegram-bot` (20.7), `pydantic` (2.5.0), `uvicorn` (0.24.0)

## 3. Frontend Technology
- **Framework**: Next.js 14.0.4 (React 18.2.0)
- **Styling**: Tailwind CSS
- **State Management/Data Fetching**: TanStack React Query (v5)
- **HTTP Client**: Axios
- **Icons**: Lucide React
- **Charts**: Recharts

## 4. Folder Structure
```text
davomatai/
├── backend/                # FastAPI Application
│   ├── database/           # SQL schemas and migrations
│   ├── models/             # SQLAlchemy models
│   ├── routes/             # API endpoints
│   ├── services/           # Business logic (Face, Attendance, Telegram)
│   ├── uploads/            # Local storage for face images
│   ├── main.py             # Entry point
│   └── Dockerfile          # Backend container config
├── frontend/               # Next.js Admin Panel
│   ├── app/                # Next.js App Router pages
│   ├── components/         # UI components
│   └── Dockerfile          # Frontend container config
├── esp32-cam/              # C++ Firmware for ESP32-CAM
├── mobile/                 # Flutter Mobile Application
├── docker-compose.yml      # Local multi-container setup
├── render.yaml             # Render.com deployment config
└── README.md               # Project overview
```

## 5. Entry Point File
- **Backend**: `backend/main.py`
- **Frontend**: `frontend/app/page.tsx` (Next.js entry)
- **ESP32-CAM**: `esp32-cam/esp32-cam.ino`

## 6. Environment Variables Used
### Backend (`backend/.env`)
- `DATABASE_URL`: PostgreSQL connection string.
- `SECRET_KEY`: Security key for token generation.
- `TELEGRAM_BOT_TOKEN`: Token from BotFather.
- `TELEGRAM_ADMIN_CHAT_IDS`: Comma-separated IDs for admin notifications.
- `INSIGHTFACE_MODEL`: Set to `buffalo_s`.
- `FACE_MATCH_THRESHOLD`: Similarity threshold (default `0.5`).
- `PORT`: Server port (default `8000`).

### Frontend (`frontend/.env.local`)
- `NEXT_PUBLIC_API_URL`: URL of the backend API.

## 7. How the Project is Currently Run
### Local Run (Manual)
- **Backend**: 
  ```bash
  cd backend
  python main.py
  ```
- **Frontend**:
  ```bash
  cd frontend
  npm run dev
  ```

### Local Run (Docker)
```bash
docker-compose up --build
```

## 8. Deployment Details
- **Docker**: Both backend and frontend have `Dockerfile`s.
- **Render.com**: Configured via `render.yaml`.
- **Build Commands**:
    - Backend: `pip install -r requirements.txt && python download_models.py`
    - Frontend: `npm install && npm run build`
- **Start Commands**:
    - Backend: `uvicorn main:app --host 0.0.0.0 --port $PORT`
    - Frontend: `npm start`

## 9. External Services Used
- **Database**: PostgreSQL (Managed service or Docker container).
- **APIs**: Telegram Bot API.
- **Cloud Hosting**: Render.com (suggested).

## 10. Known Issues & Optimizations
- **Memory Usage (Critical)**: InsightFace models are memory-intensive. 
    - **Optimization 1**: Switched from `buffalo_l` to `buffalo_s` (Lite model).
    - **Optimization 2**: `download_models.py` deletes unused `.onnx` files to save disk/RAM.
    - **Optimization 3**: Lazy loading implemented in `FaceRecognitionService` (model loads only on first request).
    - **Optimization 4**: Threading limited via `OMP_NUM_THREADS=1` to prevent CPU/RAM spikes.
- **Build Errors**: Ensure `libgl1` and `libglib2.0-0` are installed in the environment (included in `Dockerfile`).
- **Frontend Memory**: `npm run dev` is configured with `--max-old-space-size=4096` to prevent heap out-of-memory during development.
