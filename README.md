# TudoEmUm Faz-Tudo

A personal Django toolbox with private to-do lists and public web page extraction.
Python 3.12+; Django 5.2 LTS; SQLite for local development.

## Run locally

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

Settings read environment variables directly. `.env.example` documents them; `.env` files are **not** loaded automatically. Export variables in your shell or configure them in your hosting service.

Local development defaults to debug mode. Before hosting, set `DJANGO_DEBUG=false`, a persistent random `DJANGO_SECRET_KEY`, and `DJANGO_ALLOWED_HOSTS`. Run `python manage.py check --deploy`, configure HTTPS, secure cookies, static file serving, a production WSGI/ASGI server, database backups, and an outbound firewall.

The scraper rejects local/private IPs and checks redirect destinations. DNS checks alone do not prevent DNS rebinding; enforce public-only outbound access at the network layer before exposing it to untrusted users. Scraping is synchronous and intended for personal use; use background jobs and quotas for larger workloads.

## Verify

```sh
python manage.py check
python manage.py test
```
