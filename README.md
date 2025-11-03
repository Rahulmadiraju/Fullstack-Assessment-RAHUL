# Full Stack Developer Assessment — Complete Solution

This repository contains a complete full-stack deliverable for the provided assessment:
- Backend: FastAPI (Python) that accepts transaction webhooks, processes them in background (30s delay), and stores status persistently with idempotency.
- Frontend: React + TypeScript Vite app that shows imaginary analytics charts, allows updating values, and stores custom values in Supabase bound to user email.

## Overview

The system consists of:

| Layer | Tech |
|-------|------|
| Backend API | Python 3 + FastAPI |
| Queue / Async processing | asyncio tasks (30-second simulated delay) |
| DB (Local Dev) | SQLite |
| DB (Cloud Deployment) | Railway PostgreSQL |
| Frontend | React + TypeScript + Vite |
| Analytics data | Supabase table `user_values` |
| Security | Supabase RLS (3 policies) |


## Features

### Backend Capabilities
- `/v1/webhooks/transactions` → receives transaction webhooks from external payment providers
- returns an immediate ACK (fast response)
- schedules background processing that waits 30 seconds
- updates status to `PROCESSED`
- `/v1/transactions/{transaction_id}` → retrieve final status
- idempotent: same transaction id never creates duplicate
- DB persistence ensures no lost transactions

### Frontend Capabilities
- interactive UI
- user can input daily values + their email
- values stored in Supabase
- if user already exists → prompts confirmation to overwrite
- graphs update based on user inputs
- styling roughly inspired by superbryn.com

### Supabase Integration
- table: `user_values`
- schema: email + JSONB values
- RLS enabled
- anon allowed for select / insert / update

## Supabase Setup 

1. create new project: https://supabase.com
2. go to SQL → run this:

```
drop table if exists public.user_values;

create table public.user_values (
  id bigserial primary key,
  email text unique not null,
  values jsonb
);
```
3. enable RLS on table
4. create 3 policies:

| Command | Policy name | using() / with check() code |
|---------|-------------|-----------------------------|
| SELECT  | allow anon select  | true |
| INSERT  | allow anon insert  | true |
| UPDATE  | allow anon update  | true |

5. copy Supabase URL + anon key (Project → Settings → API)

## Local Backend Run :

### 1. Start backend
```
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Backend now runs at: http://127.0.0.1:8000

## Local Frontend Run :
1. Create frontend/.env.local :

```
VITE_SUPABASE_URL=<your supabase url>
VITE_SUPABASE_ANON_KEY=<your supabase anon key>
```

 2. Start Frontend In another terminal :

```
cd frontend
npm install
npm run dev

```
Frontend now runs at: http://localhost:5173/

## Deployment:

### Backend (Railway) :

1. login → https://railway.app

2. new project → Deploy from GitHub Repo

3. add env var:

```

```
4. set start command:

```

```

### Frontend (Vercel):

1. login → https://vercel.com

2. import GitHub repo

3. set envs:

```
VITE_SUPABASE_URL = <your supabase url>
VITE_SUPABASE_ANON_KEY = <your supabase anon key>
```
4. Deploy.

## Architecture Decisions :

| Topic        | Choice                     | Reason                                       |
|--------------|-----------------------------|-----------------------------------------------|
| async processing | asyncio.create_task         | no external queue required                    |
| DB           | SQLite local / Postgres deploy | SQLite zero-config for dev, Postgres for prod |
| frontend     | Vite + TS                   | fast dev cycle, simpler config                |
| supabase     | anon + RLS                  | fast MVP, no login complexity                 |
| idempotency  | DB lookup                   | simplest correct solution                     |

### Brief Explanation of Technical Choices

The tech stack was intentionally selected to meet the core requirements fast, reliably, and in a way that’s easy to reason about. FastAPI fits well because it already supports async out of the box so implementing the 30-second background processing didn’t require Celery, Redis, or any extra queue layer. For local development, SQLite keeps setup simple (especially on Windows), and for deployment it can be swapped to Postgres without code changes. The frontend uses React + Vite + TypeScript since Vite is faster to spin up and iterate with, and TS gives a bit more confidence during integration with Supabase. Supabase itself removes auth complexity I only need anonymous read/write for this assignment, and RLS policies allow that safely. Overall, the decisions here are biased toward keeping moving parts minimal while still hitting all the functional requirements cleanly.

## Assumptions :

- payment processors call webhook multiple times safely

- 30s wait is simulation, not real payment settlement

- no need for authentication on frontend for this assignment

- supabase table only stores 1 row per email

## Postman / OpenAPI
- OpenAPI YAML included as `openapi.yaml`
- Postman collection included as `postman_collection.json`

## Tests
- Backend tests: `backend/tests/test_webhooks.py` (pytest)
- Run backend tests:
```
cd backend
.\.venv\Scripts\Activate.ps1
pytest -q
```

