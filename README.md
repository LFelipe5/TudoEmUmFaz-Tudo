# TudoEmUm Faz-Tudo

A personal Django toolbox with private to-do lists and public web page extraction.
Python 3.12+; Django 5.2 LTS; SQLite for local development.

## Run with Docker (recommended)

Install Docker Desktop (Windows/macOS) or Docker Engine with the Compose plugin (Linux). No local Python or pip installation is needed.

```sh
docker compose up --build -d
docker compose exec web python manage.py createsuperuser
```

Open http://localhost:8000 and sign in with the account you just created.
The image installs all Python dependencies. Startup automatically applies database migrations.
The database and a generated secret key persist in the `toolbox_data` named volume across container restarts and rebuilds.

```sh
docker compose logs -f web       # View logs
docker compose stop              # Stop the app
docker compose up -d             # Start again
docker compose down              # Remove containers; keep data
docker compose run --rm web python manage.py test
```

`docker compose down -v` also deletes your database and saved key. Use it only when you want to reset everything.
If port 8000 is in use, change the host port in `compose.yaml` (for example `127.0.0.1:8001:8000`), then open http://localhost:8001.
After updating the code, run `docker compose up --build -d` again.

This Compose setup is for local personal use and binds only to your computer's loopback interface. It uses Django's development server. Production hosting needs the deployment configuration described below.

## Run locally without Docker

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000 and sign in. The admin is at `/admin/`.
On Windows, activate with `.venv\Scripts\activate`.

## Tools

- To-do list: add, complete, reopen, and delete your own tasks.
- Web scraper: fetch public HTML and extract its title, up to 50 headings and 100 links. Fetches have connection/read timeouts, a 1 MB response limit, and a redirect limit. JavaScript is not executed. Check site permissions, terms, and robots.txt yourself.
- Add future tools inside `core`, or create dedicated Django apps as they grow.

## Configuration

Settings read environment variables directly. `DJANGO_DB_PATH` optionally overrides the SQLite file location. `.env.example` documents them; `.env` files are **not** loaded automatically. Export variables in your shell or configure them in your hosting service.

Local development defaults to debug mode. Before hosting, set `DJANGO_DEBUG=false`, a persistent random `DJANGO_SECRET_KEY`, and `DJANGO_ALLOWED_HOSTS`. Run `python manage.py check --deploy`, configure HTTPS, secure cookies, static file serving, a production WSGI/ASGI server, database backups, and an outbound firewall.

The scraper rejects local/private IPs and checks redirect destinations. DNS checks alone do not prevent DNS rebinding; enforce public-only outbound access at the network layer before exposing it to untrusted users. Scraping is synchronous and intended for personal use; use background jobs and quotas for larger workloads.

## Verify

```sh
python manage.py check
python manage.py test
```
