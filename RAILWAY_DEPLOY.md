# Railway Deployment Guide (Gavel)

This guide deploys Gavel on Railway with:

- Web service: Flask + Gunicorn
- Worker service: Celery
- Database: Supabase PostgreSQL
- Queue/Backend: Upstash Redis

## 1. Create Supabase Database

1. Create a project in Supabase.
2. Open **Project Settings -> Database**.
3. Copy the PostgreSQL connection string.
4. Ensure the URL is PostgreSQL, for example:

```text
postgresql://postgres:<password>@<host>:5432/postgres
```

## 2. Create Upstash Redis

1. Create a Redis database in Upstash.
2. Copy the TLS Redis URL, for example:

```text
rediss://default:<password>@<host>:6379
```

## 3. Add Railway Environment Variables

In Railway, set these environment variables for both services (web and worker):

- `DATABASE_URL` = Supabase PostgreSQL URL
- `REDIS_URL` = Upstash Redis URL
- `SECRET_KEY` = long random secret
- `ADMIN_PASSWORD` = admin login password
- `BASE_URL` = public app URL, e.g. `https://your-app.up.railway.app`
- `MAIL_USERNAME` (optional)
- `MAIL_PASSWORD` (optional)

Notes:

- Environment variables override `config.yaml`.
- `DATABASE_URL` must point to PostgreSQL.
- `REDIS_URL` must be `redis://` or `rediss://`.

## 4. Deploy Repository on Railway

1. Create a new Railway project from your GitHub repository.
2. Keep Python auto-detection enabled (the repository includes `runtime.txt`).
3. Create two services from the same repository:
   - Web service command from `Procfile`: `web`
   - Worker service command from `Procfile`: `worker`
4. Deploy.

## 5. Run Database Initialization

After first deploy, initialize tables:

1. Open Railway shell for the web service.
2. Run:

```bash
python initialize.py
```

This creates required tables in Supabase PostgreSQL.

## Verification Checklist

- Web service starts with Gunicorn.
- Worker service starts with Celery.
- Logs show successful PostgreSQL and Redis connection.
- Admin can log in and judges can submit scores.
