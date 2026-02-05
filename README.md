# DarkMoney Lens

DarkMoney Lens is a full-stack investigative workspace for tracking dark money flows with a medallion architecture pipeline (Bronze → Silver → Gold → Serving).

## Stack
- Backend: Django 4 + Django REST Framework
- Frontend: Vue 3 + Vite + TypeScript + Pinia
- DB: PostgreSQL
- Orchestration: Airflow-style DAGs (optional)
- Observability: structured logs + /api/metrics endpoint

## Local Setup
```bash
docker compose up --build
```

Services:
- Backend: http://localhost:8000
- Frontend: http://localhost:5173

## Seed Credentials
- Username: `admin`
- Password: `admin1234`

## Running Pipelines Locally
```bash
python backend/manage.py run_pipeline --source=demo_resources
python backend/manage.py run_pipeline --source=demo_finance
```

## Medallion Contracts
- **Bronze**: immutable raw payloads with envelope metadata.
- **Silver**: normalized per source schema; rebuildable from Bronze.
- **Gold**: canonical entities/relationships with survivorship.
- **Serving**: app-optimized projections.

## Diagrams in UI
- Resource Directory: `frontend/public/diagrams/dark-money-resources.svg`
- Pipelines page: `frontend/public/diagrams/medallion-pipeline.svg`

## API Surface
- `/api/resources` CRUD
- `/api/cases` CRUD + `/api/cases/:id/export` PDF
- `/api/entities` CRUD + `/api/graph` import/export
- `/api/pipeline-sources` + `/api/pipeline-runs` + lineage
- `/api/metrics` for Prometheus/Grafana
