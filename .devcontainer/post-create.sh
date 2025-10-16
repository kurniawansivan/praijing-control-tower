#!/usr/bin/env bash
set -euo pipefail

# Backend Python dependencies
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
REQ
fi

python -m pip install -U pip
pip install -r requirements.txt

echo "Post-create complete (npm will be used for frontend)."
