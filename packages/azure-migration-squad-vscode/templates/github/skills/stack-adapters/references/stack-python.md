# Skill: Stack Adapter — Python

> Stack adapter for any Python application: Django, Flask, FastAPI, Tornado, Pyramid, Bottle, plain WSGI/ASGI, Celery workers, Airflow DAGs, data-science / ML workloads, Streamlit / Dash, scripts.

## When to Use

- `stack.primary_stack: python` in the Capability Matrix
- File evidence: `*.py`, `requirements.txt`, `pyproject.toml`, `setup.py`, `setup.cfg`, `Pipfile`, `poetry.lock`, `__init__.py`

## Sub-Stack Detection

| Sub-stack | Detection signal | Typical migration target |
|-----------|------------------|--------------------------|
| **Django** | `django` in requirements; `manage.py`; `settings.py`; `INSTALLED_APPS` | App Service Linux Python / Container Apps |
| **Flask** | `flask` in requirements; `app = Flask(__name__)` | App Service / Container Apps / Functions |
| **FastAPI** | `fastapi` in requirements; `app = FastAPI()` | Container Apps / Functions (Python v2 model) |
| **Tornado / Pyramid / Bottle** | matching imports | Container Apps |
| **Celery worker** | `celery` import; `@app.task` decorators | Container Apps with KEDA; or Functions for queue triggers |
| **Airflow DAGs** | `airflow.models.DAG`, `airflow.operators.*` | Azure Data Factory (managed Airflow) or Container Apps |
| **Streamlit / Dash / Gradio** | `streamlit`, `dash`, `gradio` imports | App Service / Container Apps |
| **Data-science / ML** | `numpy`, `pandas`, `scikit-learn`, `torch`, `tensorflow`, Jupyter notebooks | Azure ML / Container Apps for batch scoring |
| **Plain script** | Single-entrypoint `.py` with shebang / cron-launched | Container Apps Jobs / Functions |
| **Python 2.x** | `print` statement (no parens) at top-level; `from __future__ import`; explicit Python 2 shebang | **Migrate to Python 3.12 first** (separate workstream) |

## Python Version Detection

In priority order:

1. `pyproject.toml` → `[project] requires-python = ">=3.x"` or `[tool.poetry.dependencies] python`
2. `setup.py` → `python_requires=">=3.x"`
3. `setup.cfg` → `[options] python_requires`
4. `.python-version` file (pyenv)
5. `runtime.txt` (Heroku-style)
6. `Dockerfile` → `FROM python:3.x-...`
7. CI config → `python-version:` in GitHub Actions

If Python 2 is detected, **flag as `risk_flags: [unsupported-runtime]`** and treat Python 2→3 as a Phase 2 sub-project.

## Dependency Management

| Manager | Files | Notes |
|---------|-------|-------|
| pip + requirements.txt | `requirements.txt`, `requirements-dev.txt` | Simplest |
| Poetry | `pyproject.toml`, `poetry.lock` | Modern; lockfile-driven |
| pipenv | `Pipfile`, `Pipfile.lock` | Less common now |
| PDM | `pyproject.toml` + `pdm.lock` | Less common |
| Conda | `environment.yml`, `meta.yaml` | Common in data-science workloads |

For data-science apps with Conda dependencies, plan to either bake them into a container or use Azure ML environments.

## Probes

### Manifest inspection

- Read `pyproject.toml` (preferred) or `requirements.txt`
- Capture top dependencies (especially frameworks + native deps)
- Look for system-level requirements: `psycopg2-binary` (Postgres), `pyodbc` (ODBC drivers needed in container), `cryptography` (build deps), `lxml` (libxml2)

### Entry-point inspection

- `main.py`, `app.py`, `wsgi.py`, `asgi.py`, `manage.py`
- `if __name__ == "__main__":` blocks
- Dockerfile `CMD` line
- `Procfile` (Heroku)

### Web framework specifics

#### Django

- `settings.py` → `DATABASES`, `INSTALLED_APPS`, `MIDDLEWARE`, `STATIC_URL`, `MEDIA_URL`
- `urls.py` → routing
- `models.py` → ORM models
- Migrations in `*/migrations/`
- Custom management commands in `*/management/commands/`
- Look for `django-storages` (S3 / Azure Blob), `django-celery-beat` (scheduler)

#### Flask

- `app.py` / blueprint registration
- `flask-sqlalchemy`, `flask-login`, `flask-migrate` extensions

#### FastAPI

- `Annotated` parameters
- `BackgroundTasks`
- `@app.get/post/...`
- async / sync handler mix

### Async patterns

- `async def` + `await` → ASGI server needed (uvicorn, hypercorn, daphne)
- Pure sync → WSGI (gunicorn + workers)

### Data access

- `psycopg2` / `psycopg3` → PostgreSQL
- `pyodbc` / `pymssql` → SQL Server
- `mysqlclient` / `PyMySQL` → MySQL
- `sqlalchemy` → ORM
- `pymongo` → MongoDB
- `redis` → Redis
- `boto3` → AWS SDK (will need Azure SDK replacements)
- `google-cloud-*` → GCP SDK (will need Azure SDK replacements)
- `azure-*` packages → already Azure-aware

### Worker / task patterns

- `celery` + broker (Redis / RabbitMQ) → Container Apps + KEDA on queue depth
- `rq` (Redis Queue) → same
- `apscheduler` → in-process scheduler; consider Container Apps Jobs

### Tests

- `pytest`, `unittest`, `pytest-django`, `pytest-asyncio`
- `pyproject.toml` `[tool.pytest.ini_options]` config
- Coverage tools (`coverage.py`, `pytest-cov`)

## Phase 2 Effort Mapping

| Sub-stack | Phase 2 effort | Notes |
|-----------|----------------|-------|
| Python 3.10+ Django/Flask/FastAPI | S | Containerize, deploy |
| Python 3.7–3.9 | S–M | Minor version bump |
| Python 2.x → 3.12 | XL | Full code migration (six, futurize, manual) |
| Celery with Redis broker | M | Add managed Redis; KEDA scaling rules |
| Django with SQLite | M | Move to Azure Postgres/MySQL |
| ML / data-science (no web) | M | Containerize or move to Azure ML |
| Airflow DAGs | L | Re-host on Managed Airflow (Data Factory) or AKS |

## Identity Modernization

| Today | Target |
|-------|--------|
| Django built-in user model | Keep + integrate Entra ID via `django-azure-auth` / `django-allauth` |
| Flask-Login | Add `msal` / `authlib` + Entra ID |
| Custom JWT | Replace with Entra ID OIDC tokens |
| OAuth via social providers | Move to Entra ID External Identities |

## Target Azure Mapping

| Sub-stack | Primary Azure target | Secondary |
|-----------|----------------------|-----------|
| Django (web) | App Service Linux Python | Container Apps |
| Flask / FastAPI | App Service Linux Python | Container Apps; Functions for FastAPI v2 |
| Celery worker | Container Apps (KEDA on queue) | AKS |
| Airflow | Azure Data Factory Managed Airflow | AKS |
| Streamlit / Dash | App Service Linux Python | Container Apps |
| Plain script (cron) | Container Apps Jobs | Functions (Timer trigger) |
| ML training | Azure ML | Container Apps Jobs |
| ML scoring | Container Apps | Azure ML online endpoints |

## Anti-Patterns

- Don't deploy SQLite-backed Django to App Service for production — move to Azure Postgres / MySQL.
- Don't keep `boto3`-based S3 calls unchanged when targeting Blob Storage. Use `azure-storage-blob` (or `boto3` with custom endpoints if dual-cloud needed).
- Don't try to upgrade Python 2 → 3 inside the migration to Azure. Treat it as a separate, prior workstream.
- Don't bundle ML model artifacts >1 GB into the container image. Mount from Blob or use Azure ML model registry.
- Don't run async ASGI under gunicorn without an async worker class (`uvicorn.workers.UvicornWorker`).
- Don't preserve `DEBUG=True` in production settings during migration.

## Output Checklist

- [ ] Sub-stack identified (one of the 10 above)
- [ ] Python version captured (and flagged if 2.x)
- [ ] Dependency manager identified (pip / Poetry / pipenv / PDM / Conda)
- [ ] Top dependencies inventoried
- [ ] Entry points captured
- [ ] Web framework specifics captured (Django settings / Flask blueprints / FastAPI app)
- [ ] Sync vs async pattern captured
- [ ] Data access libraries captured
- [ ] Worker / scheduler pattern captured
- [ ] Tests inventory captured
- [ ] System-level build dependencies flagged (psycopg2-binary, pyodbc, cryptography, etc.)
- [ ] Phase 2 effort label assigned (S/M/L/XL)
- [ ] Target Azure compute candidate noted
