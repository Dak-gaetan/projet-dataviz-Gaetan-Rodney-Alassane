"""Collecte d'instantanés Vélib (disponibilité temps réel) vers data/.

Le jeu temps réel ne fournit qu'un instantané (~1500 stations). Pour atteindre
plusieurs millions de lignes, il faut accumuler des instantanés dans le temps :
ce script en récupère un toutes les COLLECT_INTERVAL_S secondes pendant
COLLECT_DURATION_MIN minutes. Il est conçu pour être relancé (un fichier par instantané).

Usage : python src/collecter_velib.py
"""
import os
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

URL = os.environ["VELIB_STATUS_URL"]
INTERVAL = int(os.getenv("COLLECT_INTERVAL_S", "300"))
DURATION_MIN = int(os.getenv("COLLECT_DURATION_MIN", "60"))
OUT = Path(os.getenv("DATA_DIR", "data")) / "velib_status"


def instantane() -> None:
    horodatage = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    reponse = requests.get(URL, timeout=60)
    reponse.raise_for_status()
    fichier = OUT / f"velib_{horodatage}.csv"
    fichier.write_bytes(reponse.content)
    print(f"[{horodatage}] {fichier.name} ({len(reponse.content) // 1024} Ko)")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    fin = time.time() + DURATION_MIN * 60
    while time.time() < fin:
        try:
            instantane()
        except requests.RequestException as e:
            print(f"Erreur réseau, on continue : {e}")
        time.sleep(INTERVAL)


if __name__ == "__main__":
    main()
