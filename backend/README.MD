# Sports Reporting Database System Backend

Flask API for the Sports Reporting Database System. This backend is configured
for a local PostgreSQL database only.

## Requirements

- Python 3.12+
- Local PostgreSQL
- Flask
- Flask SQLAlchemy
- Flask Migrate
- psycopg2 PostgreSQL driver

## Environment

Create `backend/.env` from `backend/env.example` and set the local PostgreSQL
credentials:

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/sports_event_db
```

The application keeps this standard PostgreSQL URL format. With the installed
`psycopg2` dependency, SQLAlchemy uses the psycopg2 PostgreSQL driver by
default.

## Setup

```powershell
cd backend
.\venv\bin\pip.exe install -r requirements.txt
$env:FLASK_APP='run.py'
.\venv\bin\flask.exe db upgrade -d app\migrations
.\venv\bin\python.exe seeders\scoring_type_seeder.py
.\venv\bin\python.exe run.py
```

The API runs at:

```text
http://localhost:5000/api
```

For LAN access, run the backend on the host computer and point the frontend
`VITE_API_URL` to that computer's local IP address.

## Core API Groups

- `/api/events`
- `/api/sports`
- `/api/scoring-types`
- `/api/event-sports`
- `/api/games`
- `/api/game-scores`
- `/api/criteria`
- `/api/judges`
- `/api/score-components`
- `/api/reports`

All successful responses use:

```json
{
  "success": true,
  "data": [],
  "message": "..."
}
```

All error responses use:

```json
{
  "success": false,
  "data": null,
  "message": "..."
}
```
