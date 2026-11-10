"""Collecte continue d'instantanés Vélib (disponibilité temps réel) dans data/velib_status/.

Le jeu temps réel ne donne que l'état actuel (~1 500 stations). Pour atteindre
plusieurs millions de lignes, on accumule un instantané toutes les COLLECT_INTERVAL_S
secondes. Un fichier par instantané, écrit de façon atomique : une interruption
(veille du PC, arrêt de Docker) ne corrompt rien, on relance simplement.

Usage :
    python src/collecter_velib.py            # tourne jusqu'à Ctrl+C / docker stop
    python src/collecter_velib.py --once     # un seul instantané (test)

Variables d'environnement (voir .env.example) :
    VELIB_STATUS_URL     une ou plusieurs URL CSV séparées par des virgules (essayées dans l'ordre)
    COLLECT_INTERVAL_S   secondes entre deux instantanés (défaut 120)
    COLLECT_DURATION_MIN durée maximale en minutes, 0 = illimité (défaut 0)
    DATA_DIR             dossier de données (défaut data)
"""
import argparse
import os
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

# Permalien data.gouv.fr du CSV « Vélib - Vélos et bornes, disponibilité temps réel »
DEFAULT_URL = "https://www.data.gouv.fr/api/1/datasets/r/0845c838-6f18-40c3-936f-da204107759a"
URLS = [u.strip() for u in os.getenv("VELIB_STATUS_URL", DEFAULT_URL).split(",") if u.strip()]
INTERVAL = int(os.getenv("COLLECT_INTERVAL_S", "120"))
DURATION_MIN = int(os.getenv("COLLECT_DURATION_MIN", "0"))
OUT = Path(os.getenv("DATA_DIR", "data")) / "velib_status"
OBJECTIF_LIGNES = 2_000_000
MIN_OCTETS = 10_000  # en dessous, la réponse n'est pas un vrai CSV de stations


def telecharger() -> bytes:
    """Essaie chaque URL dans l'ordre et renvoie le premier CSV valide."""
    derniere_erreur = None
    for url in URLS:
        try:
            r = requests.get(url, timeout=60)
            r.raise_for_status()
            contenu = r.content
            if len(contenu) < MIN_OCTETS or contenu.lstrip().startswith(b"<"):
                raise ValueError(f"réponse inattendue ({len(contenu)} octets, pas un CSV)")
            return contenu
        except (requests.RequestException, ValueError) as e:
            derniere_erreur = e
    raise RuntimeError(f"toutes les URL ont échoué : {derniere_erreur}")


def instantane() -> int:
    """Télécharge et enregistre un instantané. Renvoie le nombre de lignes de données."""
    contenu = telecharger()
    horodatage = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    fichier = OUT / f"velib_{horodatage}.csv"
    tmp = fichier.with_suffix(".tmp")
    tmp.write_bytes(contenu)
    tmp.replace(fichier)  # écriture atomique
    return max(contenu.count(b"\n") - 1, 0)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--once", action="store_true", help="un seul instantané puis arrêt")
    args = parser.parse_args()

    OUT.mkdir(parents=True, exist_ok=True)
    debut = time.time()
    fin = debut + DURATION_MIN * 60 if DURATION_MIN > 0 else None
    erreurs_consecutives = 0
    prochain = time.time()

    print(f"Collecte vers {OUT} toutes les {INTERVAL}s ({len(URLS)} URL). Ctrl+C pour arrêter.")
    while True:
        try:
            lignes = instantane()
            erreurs_consecutives = 0
            nb_fichiers = sum(1 for _ in OUT.glob("velib_*.csv"))
            total = lignes * nb_fichiers
            print(
                f"[{datetime.now():%Y-%m-%d %H:%M:%S}] {lignes} stations | "
                f"{nb_fichiers} instantanés | ≈ {total:,} lignes "
                f"({100 * total / OBJECTIF_LIGNES:.0f} % de l'objectif)".replace(",", " ")
            )
        except Exception as e:  # on ne s'arrête jamais sur une erreur réseau
            erreurs_consecutives += 1
            print(f"[{datetime.now():%H:%M:%S}] erreur ({erreurs_consecutives}) : {e}")

        if args.once:
            return
        if fin and time.time() >= fin:
            print("Durée maximale atteinte, arrêt.")
            return
        # cadence régulière : on compense le temps passé dans le téléchargement
        prochain += INTERVAL
        time.sleep(max(0.0, prochain - time.time()))


if __name__ == "__main__":
    main()
