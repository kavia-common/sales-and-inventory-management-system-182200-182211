#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
echo "[env] MYSQL_USER=${MYSQL_USER:-}"
echo "[env] MYSQL_HOST=${MYSQL_HOST:-}"
echo "[env] MYSQL_PORT=${MYSQL_PORT:-}"
echo "[env] MYSQL_DB=${MYSQL_DB:-}"
python check_db_connection.py || true
