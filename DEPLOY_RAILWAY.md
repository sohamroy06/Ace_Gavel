# Deploying Gavel to Railway

Step-by-step guide to deploy the Gavel judging system on [Railway](https://railway.app).

## Prerequisites

- GitHub account with this repository pushed
- [Supabase](./SUPABASE_SETUP.md) database created
- [Upstash](./UPSTASH_SETUP.md) Redis created
- Railway account (free tier works)

## Step 1: Create Railway Project

1. Go to [railway.app](https://railway.app) and sign in with GitHub
2. Click **"New Project"** → **"Deploy from GitHub Repo"**
3. Select your Gavel repository
4. Railway will auto-detect the `Procfile` and `railway.json`

## Step 2: Set Environment Variables

In your Railway project, go to **Variables** and add:

| Variable | Value | Required |
|----------|-------|----------|
| `ADMIN_PASSWORD` | Your admin password | ✅ |
| `SECRET_KEY` | Long random string (`python -c "import secrets; print(secrets.token_hex(32))"`) | ✅ |
| `DATABASE_URL` | Supabase connection string (see [SUPABASE_SETUP.md](./SUPABASE_SETUP.md)) | ✅ |
| `REDIS_URL` | Upstash Redis URL (see [UPSTASH_SETUP.md](./UPSTASH_SETUP.md)) | ✅ |
| `DISABLE_EMAIL` | `true` (set to `false` if email is configured) | ✅ |
| `IGNORE_CONFIG_FILE` | `true` | ✅ |
| `PROXY` | `true` | ✅ |
| `EMAIL_FROM` | `_unused_` (or your email) | ✅ |
| `EMAIL_USER` | `_unused_` (or your SMTP user) | ✅ |
| `EMAIL_PASSWORD` | `_unused_` (or your SMTP password) | ✅ |

### Optional Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MIN_VIEWS` | `2` | Min views before smart assignment |
| `TIMEOUT` | `5.0` | Judge timeout in minutes |
| `SEND_STATS` | `true` | Send anonymous usage stats |
| `BASE_URL` | *(auto)* | Override base URL for emails |

## Step 3: Deploy Web Service

Railway will automatically deploy from the `Procfile`. The web process runs:

```
python initialize.py && gunicorn -b 0.0.0.0:$PORT -w 4 gavel:app
```

This:
1. Creates database tables (if they don't exist)
2. Starts Gunicorn with 4 workers

## Step 4: Deploy Celery Worker

To run the Celery worker (needed for email queue):

1. In Railway, click **"New"** → **"Service"** → **"GitHub Repo"**
2. Select the same repository
3. Go to **Settings** → **Deploy** → Set **Start Command** to:
   ```
   celery -A gavel:celery worker --loglevel=info
   ```
4. Copy all the same environment variables from the web service

> **Note:** If you have `DISABLE_EMAIL=true`, the Celery worker is optional.

## Step 5: Initialize Database

The database is automatically initialized when the web service starts (`python initialize.py` in the Procfile). No manual step needed.

If you need to manually initialize:
```bash
# Set DATABASE_URL in your environment first
python initialize.py
```

## Step 6: Access Admin Panel

1. Open your Railway deployment URL
2. Navigate to `/admin/`
3. Log in with username `admin` and your `ADMIN_PASSWORD`

## Troubleshooting

### "Application Error" on first deploy
- Wait 30 seconds and refresh — Supabase free tier may need a cold-start
- Check Railway logs for specific error messages

### Database connection errors
- Verify `DATABASE_URL` is correct (must start with `postgresql://`)
- Ensure Supabase project is not paused (free tier pauses after 1 week of inactivity)

### Static files not loading
- Railway serves static files through Gunicorn — this is normal for small deployments
- For production scale, consider adding a CDN

### Email not sending
- Ensure `DISABLE_EMAIL=false` and email credentials are set
- If using Gmail, enable "App Passwords" (not "Less Secure Apps")
- Check Celery worker logs for SMTP errors
