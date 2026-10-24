#!/usr/bin/env bash
# Vérifie que l'environnement est prêt avant de lancer les notebooks.
cd "$(dirname "$0")/.."

ok()   { echo "  [OK]  $1"; }
ko()   { echo "  [KO]  $1"; FAIL=1; }
FAIL=0

echo "== Outils =="
command -v docker >/dev/null && ok "docker" || ko "docker introuvable"
docker compose version >/dev/null 2>&1 && ok "docker compose" || ko "docker compose introuvable"
command -v git >/dev/null && ok "git" || ko "git introuvable"

echo "== Configuration =="
[ -f .env ] && ok ".env présent" || ko ".env manquant (cp .env.example .env)"

echo "== Services =="
for c in velib-rustfs velib-postgres velib-jupyter velib-dashboard; do
  state=$(docker inspect -f '{{.State.Status}}' "$c" 2>/dev/null)
  [ "$state" = "running" ] && ok "$c" || ko "$c ($state)"
done

echo "== Données =="
n=$(ls data/velib_status 2>/dev/null | wc -l)
[ "$n" -gt 0 ] && ok "$n instantané(s) dans data/velib_status" || ko "aucune donnée (scripts/telecharger_donnees.sh)"

exit $FAIL
