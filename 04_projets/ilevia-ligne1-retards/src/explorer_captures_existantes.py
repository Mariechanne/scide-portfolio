"""
Exploration de toutes les captures brutes SIRI deja enregistrees (400
fichiers, 24-26/09/2026) : recherche de statuts de depart autres que
onTime/noReport (un vrai cas de retard, peut-etre), et verification de
la presence d'un champ d'horaire theorique (AimedDepartureTime) sur
l'ensemble des snapshots, pas juste celui deja inspecte manuellement.
"""

import xml.etree.ElementTree as ET
from pathlib import Path
from collections import Counter

DOSSIER_BRUT = Path("data/raw/gtfs_rt/siri_raw")
ns = {"siri": "http://www.siri.org.uk/siri"}
lignes_metro = {"ILEVIA:Line::M1:LOC", "ILEVIA:Line::RME1:LOC"}

fichiers = sorted(DOSSIER_BRUT.glob("siri_*.xml"))
print(f"Nombre de fichiers captures a analyser : {len(fichiers)}\n")

compteur_statuts = Counter()
visites_avec_aimed = 0
total_visites_metro = 0
exemple_rme1 = None
exemple_m1 = None

for fichier in fichiers:
    racine = ET.parse(fichier).getroot()
    for v in racine.findall(".//siri:MonitoredStopVisit", ns):
        line_ref = v.find(".//siri:LineRef", ns)
        if line_ref is None or line_ref.text not in lignes_metro:
            continue

        total_visites_metro += 1
        statut = v.find(".//siri:DepartureStatus", ns)
        compteur_statuts[statut.text if statut is not None else "absent"] += 1

        aimed = v.find(".//siri:AimedDepartureTime", ns)
        if aimed is not None:
            visites_avec_aimed += 1

        # On garde un exemple de chaque reference pour inspection ulterieure
        if line_ref.text == "ILEVIA:Line::RME1:LOC" and exemple_rme1 is None:
            exemple_rme1 = (fichier.name, v)
        if line_ref.text == "ILEVIA:Line::M1:LOC" and exemple_m1 is None:
            exemple_m1 = (fichier.name, v)

print(f"Total de visites metro (M1 + RME1) cumulees : {total_visites_metro}\n")
print("Repartition des DepartureStatus rencontres :")
for statut, nb in compteur_statuts.most_common():
    print(f"- {statut} : {nb}")

print(f"\nNombre de visites avec un AimedDepartureTime present : {visites_avec_aimed}")

if exemple_rme1:
    print(f"\nExemple RME1 trouve dans {exemple_rme1[0]} :")
    print(ET.tostring(exemple_rme1[1], encoding="unicode")[:500])