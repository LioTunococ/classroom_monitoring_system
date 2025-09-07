Deployment quickstart (Linux)

1) Environment
- Set environment variables (example with systemd):

  DJANGO_DEBUG=false
  DJANGO_SECRET_KEY=replace-with-strong-random
  DJANGO_ALLOWED_HOSTS=your.domain.com,www.your.domain.com
  # Optional Postgres
  DJANGO_DB_ENGINE=django.db.backends.postgresql
  DJANGO_DB_NAME=cms
  DJANGO_DB_USER=cms
  DJANGO_DB_PASSWORD=secret
  DJANGO_DB_HOST=127.0.0.1
  DJANGO_DB_PORT=5432

2) Install and build
- python -m venv .venv && source .venv/bin/activate
- pip install -r requirements.txt
- python manage.py migrate
- python manage.py collectstatic --noinput

3) Run with Gunicorn
- See gunicorn.service for a systemd unit example.

4) Nginx
- See nginx.conf.sample. It proxies to gunicorn (127.0.0.1:8000) and serves /static/ from collected files.

5) Logs
- When DEBUG=false, logs go to logs/app.log (rotating). Ensure the folder is writable by the app user.

6) Backups
- Schedule daily pg_dump (for Postgres) and keep recent copies.


Windows pilot (PowerShell)

- One‑shot script that prepares env and runs a production WSGI server (waitress):

  .\.venv\Scripts\Activate.ps1
  # Basic: local pilot without HTTPS (for LAN testing). Do NOT use on the public Internet.
  powershell -ExecutionPolicy Bypass -File deploy\setup-and-run.ps1 -Domain "localhost" -Https:$false -Port 8000

  # Production posture behind HTTPS (proxy/host terminates TLS) for your domain(s):
  powershell -ExecutionPolicy Bypass -File deploy\setup-and-run.ps1 -Domain "yourdomain.com,www.yourdomain.com" -Https:$true -Port 8000

- Notes:
  - When -Https is used, the script enables SSL redirect and HSTS; ensure your site is served over HTTPS by a reverse proxy (Nginx/IIS/ELB) that forwards to waitress on 127.0.0.1:8000.
  - The script generates a strong DJANGO_SECRET_KEY if you don’t pass one; to pin a value, add -Secret "...".
  - You can still use the Linux artifacts (gunicorn + nginx) if you deploy on a Linux host.
