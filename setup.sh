#!/usr/bin/env bash
set -euo pipefail

error() { printf '%s\n' "$*" >&2; exit 1; }
root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
action=${1:-up}
case "$action" in
  up|doctor|health|reset|down|install) ;;
  *) error 'Usage: ./scripts/setup.sh [up|doctor|health|reset|down|install [directory]]' ;;
esac
command -v docker >/dev/null || error 'Install Docker Desktop or Docker Engine with Compose v2.'
docker compose version >/dev/null 2>&1 || error 'Install the Docker Compose v2 plugin.'
docker info >/dev/null 2>&1 || error 'Start Docker and confirm your account can run docker info.'

# This mode also works when this file is downloaded by itself.
if [[ "$action" == install ]]; then
  command -v git >/dev/null || error 'Install Git to clone the release.'
  destination=${2:-ThreatHuntX}
  [[ ! -e "$destination" ]] || error "Choose an absent install directory. Run ./scripts/setup.sh inside an existing checkout."
  git clone --depth 1 --branch v0.1.0 https://github.com/Aventador-LP700/ThreatHuntX.git -- "$destination"
  exec bash "$destination/scripts/setup.sh" up
fi

cd -- "$root"
[[ -f compose.yaml && -r scenarios/fixtures/02.positive.json ]] || error 'Run from a complete checkout or pass install to clone the release.'
case "$action" in
  down) docker compose down; exit ;;
  reset) docker compose exec -T api python -m app.cli reset; exit ;;
  health) docker compose ps; docker compose exec -T web wget -Y off -qO - http://127.0.0.1:8080/api/health; printf '\n'; exit ;;
esac

docker compose config --quiet
port=$(docker compose config | awk '/published:/{gsub(/"/, "", $2); print $2; exit}')
[[ "$port" =~ ^[1-9][0-9]{0,4}$ && "$port" -le 65535 ]] || error 'Use a THREATHUNTX_PORT from 1 through 65535 in .env.'
if ! docker compose ps --status running -q web | grep -q .; then
  if (exec 3<>"/dev/tcp/127.0.0.1/$port") 2>/dev/null; then
    error "Port $port already accepts connections. Set THREATHUNTX_PORT in .env or in your shell."
  fi
fi
memory=$(docker info --format '{{.MemTotal}}')
free_kib=$(df -Pk . | awk 'NR==2 { print $4 }')
printf 'Docker resources: '
docker info --format '{{.NCPU}} CPUs, {{.MemTotal}} bytes RAM'
printf 'Free space on the checkout filesystem: %s KiB.\n' "$free_kib"
if [[ "$memory" -lt 536870912 ]]; then printf 'Low Docker memory detected. Building may require more memory.\n' >&2; fi
if [[ "$free_kib" -lt 524288 ]]; then printf 'Low free space detected. Check Docker image and build-cache storage.\n' >&2; fi
printf 'Fixture and Compose configuration are readable.\n'
if [[ "$action" == doctor ]]; then exit; fi
if ! docker compose up -d --build --wait --wait-timeout 120; then
  docker compose ps -a
  error 'The lab did not become healthy. Run docker compose logs api web for details.'
fi
printf 'Lab: http://127.0.0.1:%s/\nHealth: http://127.0.0.1:%s/api/health\n' "$port" "$port"
