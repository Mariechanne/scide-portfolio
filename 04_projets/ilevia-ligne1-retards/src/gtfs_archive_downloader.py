"""
gtfs_archive_downloader.py

Utilitaire reutilisable : telecharge une version archivee du GTFS statique
ilevia a une date donnee, via l'API publique de transport.data.gouv.fr.

Usage :
    python src/gtfs_archive_downloader.py 2026-09-16

Sert a reconstituer, retrospectivement, le calendrier theorique tel qu'il
etait publie a un instant precis (utile par exemple pour verifier si un
jour donne etait declare comme un jour de service "normal" avant un incident).
"""

import sys
import io
import zipfile
from pathlib import Path

import requests

DATASET_ID = "665fe73f1da7949369f23bb5"  # "Reseau urbain ilevia" sur transport.data.gouv.fr
RESOURCE_ID_GTFS_STATIQUE = 81995         # ressource GTFS statique (pas le temps reel, pas SIRI)


def trouver_version_archivee(date_cible: str) -> dict:
    """Cherche, dans l'historique du jeu de donnees, la version dont le
    download_datetime commence par date_cible (format 'AAAA-MM-JJ')."""
    reponse = requests.get(
        f"https://transport.data.gouv.fr/api/datasets/{DATASET_ID}", timeout=30
    )
    reponse.raise_for_status()
    historique_gtfs = [
        h for h in reponse.json().get("history", [])
        if h.get("resource_id") == RESOURCE_ID_GTFS_STATIQUE
    ]
    return next(
        h for h in historique_gtfs
        if h["payload"]["download_datetime"].startswith(date_cible)
    )


def telecharger_et_extraire(version: dict, dossier_destination: Path) -> list:
    """Telecharge l'archive zip d'une version et l'extrait dans dossier_destination."""
    url_archive = version["payload"]["permanent_url"]
    reponse_zip = requests.get(url_archive, timeout=60)
    reponse_zip.raise_for_status()

    dossier_destination.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(io.BytesIO(reponse_zip.content)) as archive:
        archive.extractall(dossier_destination)
        return archive.namelist()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage : python src/gtfs_archive_downloader.py AAAA-MM-JJ")
        sys.exit(1)

    date_demandee = sys.argv[1]
    version = trouver_version_archivee(date_demandee)
    print(f"Version trouvee, publiee le : {version['payload']['download_datetime']}")

    destination = Path(f"data/raw/gtfs_static_archive_{date_demandee.replace('-', '')}")
    fichiers = telecharger_et_extraire(version, destination)

    print(f"\nFichiers extraits dans {destination} :")
    print(fichiers)