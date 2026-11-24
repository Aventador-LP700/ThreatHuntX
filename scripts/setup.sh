#!/usr/bin/env bash
set -euo pipefail

cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.."
error() { printf '%s\n' "$*" >&2; exit 1; }
command -v docker >/dev/null || error 'Install Docker Desktop or Docker Engine with Compose v2.'
docker compose version >/dev/null 2>&1 || error 'Install the Docker Compose v2 plugin.'
docker info >/dev/null 2>&1 || error 'Start Docker and confirm your account can run docker info.'

action=${1:-up}
case "$action" in
  down) docker compose down; exit ;;
  reset) docker compose exec -T api python -m app.cli reset; exit ;;
  health) docker compose ps; exit ;;
  up|doctor) ;;
  *) error 'Usage: ./scripts/setup.sh [up|doctor|health|reset|down]' ;;
esac

docker compose config --quiet
# Compose expands .env values itself. Read its resolved port without a container.
port=$(docker compose config | awk '/published:/{gsub(/"/, "", $2); print $2; exit}')
[[ "$port" =~ ^[0-9]+$ ]] || error 'Use a numeric THREATHUNTX_PORT in .env.'
[[ -r scenarios/fixtures/02.positive.json ]] || error 'The MFA fixture is missing. Run this from a complete checkout.'
if command -v curl >/dev/null && ! docker compose ps --status running -q web | grep -q .; then
  if curl --silent --max-time 2 --output /dev/null "http://127.0.0.1:$port/"; then
    error "Local port $port is in use. Set THREATHUNTX_PORT in .env or in your shell."
  fi
fi
printf 'Docker resources: '
docker info --format '{{.NCPU}} CPUs, {{.MemTotal}} bytes RAM'
printf 'Available space in the checkout filesystem:\n'
df -h .
printf 'Fixture and Compose configuration are readable.\n'
if [[ "$action" == doctor ]]; then exit; fi
if ! docker compose up -d --build --wait --wait-timeout 120; then
  docker compose ps
  error 'The lab did not become healthy. Run docker compose logs api web for details.'
fi
printf 'Lab: http://127.0.0.1:%s/\nHealth: http://127.0.0.1:%s/api/health\n' "$port" "$port"
