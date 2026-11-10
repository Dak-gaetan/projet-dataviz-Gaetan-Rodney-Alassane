#!/usr/bin/env bash
# Télécharge les données du projet dans ./data (non versionné).
# Usage : bash scripts/telecharger_donnees.sh
set -euo pipefail

cd "$(dirname "$0")/.."
[ -f .env ] && set -a && . ./.env && set +a

mkdir -p data/velib_status data/stations

echo "==> Emplacement des stations (référentiel)"
# TODO : renseigner l'URL exacte du jeu "velib-emplacement-des-stations" sur opendata.paris.fr
STATIONS_URL="${VELIB_STATIONS_URL:-https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/velib-emplacement-des-stations/exports/csv?delimiter=%3B}"
curl -fL --retry 3 -o data/stations/stations.csv "$STATIONS_URL" \
  || echo "   (référentiel indisponible : URL à vérifier, le reste du script continue)"

echo "==> Premier instantané de disponibilité"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
curl -fL --retry 3 -o "data/velib_status/velib_${STAMP}.csv" "$VELIB_STATUS_URL"

echo "==> Pour accumuler l'historique (>= 2 M de lignes), lancer la collecte :"
echo "    python src/collecter_velib.py   (ou en tâche de fond : nohup python src/collecter_velib.py &)"
echo "Terminé. Fichiers dans ./data"
