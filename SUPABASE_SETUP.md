# Supabase Setup for Gavel

Guide to create a free PostgreSQL database on [Supabase](https://supabase.com) for Gavel.

## Step 1: Create Supabase Account

1. Go to [supabase.com](https://supabase.com) and sign up (GitHub login works)
2. Click **"New Project"**

## Step 2: Create Project

| Field | Value |
|-------|-------|
| **Organization** | Select or create one |
| **Project Name** | `gavel-judging` (or any name) |
| **Database Password** | Generate a strong password — **save this!** |
| **Region** | Choose closest to your users |
| **Plan** | Free (sufficient for 150+ teams) |

Click **"Create new project"** and wait ~2 minutes for provisioning.

## Step 3: Get Connection String

1. Go to **Project Settings** → **Database**
2. Under **Connection string**, select **URI**
3. Copy the connection string — it looks like:
   ```
   postgresql://postgres.[project-ref]:[password]@aws-0-[region].pooler.supabase.com:6543/postgres
   ```
4. Replace `[password]` with the database password you set in Step 2

> **Important:** Use the **Transaction** connection pooler (port `6543`) for web apps. The direct connection (port `5432`) is for migrations only.

## Step 4: Set in Railway

Set the `DATABASE_URL` environment variable in Railway to the connection string from Step 3.

## Free Tier Limits

| Resource | Limit |
|----------|-------|
| Database size | 500 MB |
| API requests | Unlimited |
| Bandwidth | 5 GB |
| Pause after inactivity | 1 week |

These limits are more than sufficient for a hackathon with 150+ teams and ~50 judges.

## Notes

- **Pausing:** Free-tier projects pause after 1 week of inactivity. Visit the Supabase dashboard to unpause before your hackathon.
- **Backups:** Supabase provides daily backups on paid plans. For free tier, you can manually export data from the admin panel.
- **Tables:** Gavel will automatically create all required tables when `initialize.py` runs.
