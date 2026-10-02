"""
Test decisif : le contenu des entrees M1/RME1 varie-t-il d'un fichier
a l'autre (meme avec un RecordedAtTime fige), ou les entrees sont-elles
strictement identiques d'une capture a l'autre, signe d'un flux mort
pour le metro ?
"""

import xml.etree.ElementTree as ET
from pathlib import Path

DOSSIER_BRUT = Path("data/raw/gtfs_rt/siri_raw")
ns = {"siri": "http://www.siri.org.uk/siri"}
lignes_metro = {"ILEVIA:Line::M1:LOC", "ILEVIA:Line::RME1:LOC"}

fichiers = sorted(DOSSIER_BRUT.glob("siri_*.xml"))

# On compare le tout premier et le tout dernier fichier de la serie dense
# (24/09 20h02 vs 25/09 08h24), espaces de plus de 12 heures.
premier, dernier = fichiers[0], fichiers[-2]  # -2 pour eviter la capture isolee du 26/09

def extraire_identifiants(fichier):
    racine = ET.parse(fichier).getroot()
    identifiants = []
    for v in racine.findall(".//siri:MonitoredStopVisit", ns):
        line_ref = v.find(".//siri:LineRef", ns)
        if line_ref is None or line_ref.text not in lignes_metro:
            continue
        item_id = v.find(".//siri:ItemIdentifier", ns)
        expected = v.find(".//siri:ExpectedDepartureTime", ns)
        identifiants.append((
            item_id.text if item_id is not None else "?",
            expected.text if expected is not None else "?",
        ))
    return identifiants

ids_premier = extraire_identifiants(premier)
ids_dernier = extraire_identifiants(dernier)

print(f"Fichier 1 : {premier.name} -> {len(ids_premier)} entrees M1/RME1")
for item_id, expected in ids_premier:
    print(f"  - {item_id} | depart prevu : {expected}")

print(f"\nFichier 2 : {dernier.name} -> {len(ids_dernier)} entrees M1/RME1")
for item_id, expected in ids_dernier:
    print(f"  - {item_id} | depart prevu : {expected}")

print(f"\nLes deux fichiers sont-ils strictement identiques pour M1/RME1 ? "
      f"{ids_premier == ids_dernier}")