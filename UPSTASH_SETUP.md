# Upstash Redis Setup for Gavel

Guide to create a free Redis instance on [Upstash](https://upstash.com) for Celery task queue.

## Step 1: Create Upstash Account

1. Go to [upstash.com](https://upstash.com) and sign up
2. Navigate to **Redis** → **Create Database**

## Step 2: Create Redis Database

| Field | Value |
|-------|-------|
| **Name** | `gavel-redis` (or any name) |
| **Type** | Regional |
| **Region** | Choose closest to your Railway deployment |
| **TLS** | Enabled (default) |
| **Eviction** | Disabled |

Click **"Create"**.

## Step 3: Get Connection String

1. On the database details page, find **Redis Connect**
2. Copy the `REDIS_URL` — it looks like:
   ```
   rediss://default:your-password@your-endpoint.upstash.io:6379
   ```

> **Note:** The URL starts with `rediss://` (with double 's') for TLS connections.

## Step 4: Set in Railway

Set the `REDIS_URL` environment variable in Railway to the connection string from Step 3.

## What Redis is Used For

Gavel uses Redis as a **Celery message broker** for:
- Sending invitation emails asynchronously
- Background task processing

If you have `DISABLE_EMAIL=true`, Redis is still needed for the Celery broker but will have minimal usage.

## Free Tier Limits

| Resource | Limit |
|----------|-------|
| Commands | 10,000/day |
| Storage | 256 MB |
| Connections | 1,000 concurrent |

This is more than sufficient for hackathon email queuing.

## Troubleshooting

### Connection refused
- Ensure you're using `rediss://` (TLS) not `redis://`
- Check that TLS is enabled on the Upstash database

### Celery worker not connecting
- Verify `REDIS_URL` is set in the Celery worker service (not just the web service)
- Check Railway logs for connection errors
