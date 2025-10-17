#!/usr/bin/env bash
set -euo pipefail

cd /workspaces/praijing-control-tower/backend
if [ ! -f requirements.txt ]; then
  cat > requirements.txt <<'REQ'
fastapi==0.115.2
uvicorn[standard]==0.30.6
pydantic==2.9.2
pytest==8.3.3
httpx==0.27.2
ruff==0.6.8
mypy==1.13.0
SQLAlchemy==2.0.44
alembic==1.17.0
psycopg2-binary==2.9.11
pydantic-settings==2.11.0
REQ
fi

python -m pip install -U pip
pip install -r requirements.txt

echo "Post-create complete."