"""
Capture brute du flux SIRI SM, horodatee, sans transformation.
Chemin ancre sur l'emplacement du script (pas sur le dossier de travail
courant), necessaire pour fonctionner correctement une fois lance par
le Planificateur de taches Windows.
"""

from pathlib import Path
from datetime import datetime, timezone
import requests

RACINE_PROJET = Path(__file__).resolve().parent.parent
DOSSIER_BRUT = RACINE_PROJET / "data" / "raw" / "gtfs_rt" / "siri_raw"
DOSSIER_BRUT.mkdir(parents=True, exist_ok=True)

URL_SIRI = "https://proxy.transport.data.gouv.fr/resource/ilevia-lille-siri-sm"

reponse = requests.get(URL_SIRI, timeout=60)
reponse.raise_for_status()

horodatage = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
chemin_fichier = DOSSIER_BRUT / f"siri_{horodatage}.xml"
chemin_fichier.write_bytes(reponse.content)

print(f"Snapshot enregistre : {chemin_fichier} ({len(reponse.content)} octets)")