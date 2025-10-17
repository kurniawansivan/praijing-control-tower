#!/usr/bin/env bash
set -euo pipefail

# Find the installed Postgres major version (highest available)
PGVER=$(ls /usr/lib/postgresql 2>/dev/null | sort -V | tail -n1)
if [ -z "${PGVER:-}" ]; then
  echo "PostgreSQL binaries not found. Is it installed?" >&2
  exit 1
fi

# Ensure a 'main' cluster exists; create it if missing
if ! sudo pg_lsclusters | awk 'NR>1{print $1,$2}' | grep -qE "^${PGVER}\s+main$"; then
  echo "Creating PostgreSQL cluster ${PGVER}/main..."
  sudo pg_createcluster "$PGVER" main --start
fi

# Ensure config allows connections on localhost with password auth
CONF="/etc/postgresql/${PGVER}/main/postgresql.conf"
HBA="/etc/postgresql/${PGVER}/main/pg_hba.conf"

# Listen on all interfaces (we'll forward 5432)
sudo sed -i "s/^#\?listen_addresses.*/listen_addresses = '*'/" "$CONF"

# Add localhost password rules if missing
if ! sudo grep -qE '^host\s+all\s+all\s+127\.0\.0\.1/32\s+md5' "$HBA"; then
  echo "host all all 127.0.0.1/32 md5" | sudo tee -a "$HBA" >/dev/null
fi
if ! sudo grep -qE '^host\s+all\s+all\s+::1/128\s+md5' "$HBA"; then
  echo "host all all ::1/128 md5" | sudo tee -a "$HBA" >/dev/null
fi

# Start cluster if not online
if ! sudo pg_lsclusters | awk -v v="$PGVER" '$1==v && $2=="main" {print $4}' | grep -q online; then
  echo "Starting PostgreSQL cluster ${PGVER}/main..."
  sudo pg_ctlcluster "$PGVER" main start
else
  sudo pg_ctlcluster "$PGVER" main reload
fi

# Ensure role and database exist
if ! sudo -u postgres psql -tc "SELECT 1 FROM pg_roles WHERE rolname='app'" | grep -q 1; then
  sudo -u postgres psql -c "CREATE ROLE app LOGIN PASSWORD 'app';"
fi
if ! sudo -u postgres psql -tc "SELECT 1 FROM pg_database WHERE datname='praijing'" | grep -q 1; then
  sudo -u postgres psql -c "CREATE DATABASE praijing OWNER app;"
fi

echo "PostgreSQL is ready at localhost:5432 (db=praijing, user=app, pass=app)"
