# Enterprise-Grade FastAPI Folder Structure

Researched from the best open-source FastAPI projects:

- [zhanymkanov/fastapi-best-practices](https://github.com/zhanymkanov/fastapi-best-practices) (~13k★) — conventions from a production startup
- [Netflix/dispatch](https://github.com/Netflix/dispatch) — the structure the above is based on; Netflix's real production FastAPI app
- [fastapi/full-stack-fastapi-template](https://github.com/fastapi/full-stack-fastapi-template) (~35k★) — the official template by FastAPI's creator

**The consensus:** organize by **domain (feature)**, not by file type. File-type layout
(`routers/`, `services/`, `models/` at the top) works for small services, but every
production monolith that scaled (Netflix Dispatch, zhanymkanov's startup) moved to
domain packages — because a change to "payments" touches one folder, not seven.

---

## The recommended structure

```
fastapi-project/
├── src/                          # single top-level package (import root)
│   ├── main.py                   # app factory: create_app(), mount routers, middleware
│   │
│   ├── core/                     # shared infrastructure (global, cross-domain)
│   │   ├── config.py             # pydantic-settings BaseSettings, reads .env
│   │   ├── database.py           # engine, async session factory
│   │   ├── models.py             # shared model bases/mixins (id, created_at, updated_at)
│   │   ├── schemas.py            # shared pydantic bases (ORM config, camelCase alias)
│   │   ├── exceptions.py         # global exception classes + handlers
│   │   ├── dependencies.py       # global deps: get_db
│   │   ├── pagination.py         # shared pagination params/response
│   │   └── logging.py            # structured logging setup
│   │
│   └── domains/                  # one package per business domain
│       ├── auth/
│       │   ├── router.py         # endpoints (thin — no business logic here)
│       │   ├── schemas.py        # pydantic request/response models
│       │   ├── service.py        # business logic (the only place it lives)
│       │   ├── dependencies.py   # domain deps: get_current_user, require_admin
│       │   ├── exceptions.py     # InvalidCredentials, InvalidToken, ...
│       │   ├── config.py         # domain-specific settings (JWT secret, TTLs)
│       │   └── utils.py          # hashing, token helpers
│       │
│       ├── users/                # same file set — every domain looks identical
│       │   ├── router.py
│       │   ├── schemas.py
│       │   ├── models.py         # SQLAlchemy ORM models
│       │   ├── service.py
│       │   └── exceptions.py     # only create the files a domain actually needs
│       │
│       ├── payments/             # (example) domain wrapping an external provider
│       │   ├── client.py         # external API client (stripe etc.)
│       │   ├── router.py
│       │   ├── schemas.py
│       │   ├── service.py
│       │   └── exceptions.py
│       │
│       └── tasks/                # (example) background jobs (celery/arq/taskiq)
│           ├── broker.py
│           └── email.py
│
├── tests/                        # mirrors src/ layout
│   ├── conftest.py               # app + db fixtures, test client
│   ├── auth/
│   │   └── test_login.py
│   └── users/
│       └── test_users.py
│
├── alembic/                      # DB migrations
│   └── versions/
├── alembic.ini
│
├── scripts/                      # one-off ops scripts (seed db, create superuser)
│
├── .env.example                  # documented env vars (never commit .env)
├── pyproject.toml                # deps + tool config (ruff, mypy, pytest) in ONE file
├── Dockerfile
├── docker-compose.yml            # app + postgres + redis for local dev
├── .github/workflows/ci.yml     # lint, typecheck, test on every PR
└── README.md
```

---

## The rules that make it work

1. **Routers are thin.** A router validates input (via schema), calls one service
   function, returns a schema. If a router has an `if` about business state, that
   logic belongs in `service.py`.

2. **Services own business logic.** `service.py` talks to the DB and other services.
   No HTTP objects (`Request`, `HTTPException`) inside services — raise domain
   exceptions from `exceptions.py` and map them to HTTP in a global handler.

3. **Cross-domain imports are explicit** (zhanymkanov rule):
   ```python
   from src.domains.auth import service as auth_service
   from src.domains.payments.schemas import PaymentOut
   ```
   Never wildcard, never deep-reach into another domain's `models.py` for queries —
   call its service instead.

4. **Every domain has the same file names.** New engineers learn the pattern once.
   Only create the files a domain needs — an empty `utils.py` is noise.

5. **Config is pydantic-settings, loaded once.** `src/core/config.py` for global,
   `src/domains/<domain>/config.py` only when a domain has its own knobs.

6. **Dependencies do validation.** `valid_post_id` dependency fetches the row and
   404s in one place; every endpoint that needs a post reuses it (and FastAPI
   caches it per-request).

7. **Async routes must not block.** Sync SDK call inside `async def` freezes the
   event loop — use an async client or make the route `def` (FastAPI threadpools it).

8. **Tests mirror `src/`.** A failing `tests/payments/test_refund.py` tells you the
   folder to open.

## What was deliberately left out

- **`repositories/` layer** — Dispatch and zhanymkanov both skip it; `service.py`
  using SQLAlchemy directly is one less indirection. Add a repository only when you
  genuinely swap storage backends.
- **`utils/`, `helpers/`, `common/` dumping grounds** — shared code gets a named
  module (`pagination.py`) or lives in the domain that owns it.
- **Microservice split** — this domain layout IS the migration path: each `src/domains/<domain>/`
  package can be lifted out into its own service later.

## When to use file-type layout instead

The layered layout already in `app/` here (`routers/`, `services/`, `models/` at top
level) is fine for a **small microservice with one responsibility** — the official
FastAPI docs use it for exactly that. The moment you have 3+ business domains in one
codebase, switch to the domain structure above.

## Sources

- https://github.com/zhanymkanov/fastapi-best-practices
- https://github.com/Netflix/dispatch
- https://github.com/fastapi/full-stack-fastapi-template
- https://fastapi.tiangolo.com/project-generation/
