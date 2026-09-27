# Production Deployment Guide

## Architecture Overview
The SANKALP platform must be deployed using a robust architecture:
- **Frontend**: React/Vite served statically via Nginx or a CDN.
- **Backend**: FastAPI run via Gunicorn/Uvicorn, proxied behind Nginx/HTTPS.
- **Database**: PostgreSQL (with PostGIS) on an isolated internal network.
- **Rate Limiting**: Redis configured for distributed rate limiting (via `slowapi`).

## Pre-Deployment Checklist
Before deploying the application, ensure the following are configured via the environment:
1. `APP_ENV=production`
2. `APP_DEBUG=False`
3. `CORS_ALLOWED_ORIGINS` is strictly set to the production frontend domain (e.g., `https://dashboard.sankalp.gov`).
4. `JWT_SECRET_KEY` is replaced with a cryptographically secure 256-bit key.
5. `DATABASE_URL` uses the `sankalp_app` low-privilege role.

## Running Migrations Safely
Alembic migrations should be executed as part of the CI/CD pipeline using the `sankalp_admin` role.
```bash
python -m alembic upgrade head
```
Never modify production tables manually.

## Starting the Backend
Use an ASGI server like Uvicorn managed by Gunicorn:
```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 127.0.0.1:8000
```
Then configure a reverse proxy (e.g., Nginx) to terminate HTTPS and forward requests to `127.0.0.1:8000`.
