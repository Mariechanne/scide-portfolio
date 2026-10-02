"""
Controle : la staleness de RecordedAtTime est-elle specifique au metro
(M1/RME1), ou generalisee a tout le flux SIRI d'ilevia, bus compris ?
Meme logique que le script precedent, applique a une ligne de bus
choisie au hasard comme temoin.
"""

import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime, timezone

DOSSIER_BRUT = Path("data/raw/gtfs_rt/siri_raw")
ns = {"siri": "http://www.siri.org.uk/siri"}
LIGNE_TEMOIN = "ILEVIA:Line::53:LOC"  # une ligne de bus quelconque, vue plus tot dans la session

fichiers = sorted(DOSSIER_BRUT.glob("siri_*.xml"))[:20]  # 20 fichiers suffisent pour un controle

ecarts_minutes = []

for fichier in fichiers:
    horodatage_fichier = datetime.strptime(
        fichier.stem.replace("siri_", ""), "%Y%m%dT%H%M%SZ"
    ).replace(tzinfo=timezone.utc)

    racine = ET.parse(fichier).getroot()
    for v in racine.findall(".//siri:MonitoredStopVisit", ns):
        line_ref = v.find(".//siri:LineRef", ns)
        if line_ref is None or line_ref.text != LIGNE_TEMOIN:
            continue

        recorded = v.find(".//siri:RecordedAtTime", ns)
        if recorded is None:
            continue

        horodatage_record = datetime.fromisoformat(recorded.text)
        ecart = (horodatage_fichier - horodatage_record).total_seconds() / 60
        ecarts_minutes.append(ecart)

if not ecarts_minutes:
    print(f"Aucun enregistrement trouve pour {LIGNE_TEMOIN} dans ces fichiers.")
else:
    ecarts_minutes.sort()
    n = len(ecarts_minutes)
    print(f"Ligne temoin : {LIGNE_TEMOIN}")
    print(f"Nombre d'enregistrements analyses : {n}")
    print(f"Ecart minimum : {ecarts_minutes[0]:.1f} min")
    print(f"Ecart median  : {ecarts_minutes[n // 2]:.1f} min")
    print(f"Ecart maximum : {ecarts_minutes[-1]:.1f} min")