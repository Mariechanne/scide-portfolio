"""
collecte_m1_siri.py

Interroge le flux SIRI SM d'ilevia une seule fois, extrait les visites
concernant M1 et RME1, et les ajoute en une ligne CSV compacte par
visite, plutot que de sauvegarder le XML complet (environ 7 Mo, tout
le reseau, dont on a determine qu'on n'avait besoin que d'une fraction).

Deux horodatages distincts, volontairement :
- horodatage_collecte : quand CE script a interroge le flux (GitHub Actions)
- recorded_at_time : quand le flux dit avoir mis a jour l'info lui-meme,
  indispensable pour detecter les entrees figees ("zombies") decouvertes
  le 02/10/2026, ou les deux horodatages divergent fortement.

Usage :
    python src/collecte_m1_siri.py
"""

import csv
from datetime import datetime, timezone
from pathlib import Path

import requests
import xml.etree.ElementTree as ET

URL_SIRI = "https://proxy.transport.data.gouv.fr/resource/ilevia-lille-siri-sm"
ns = {"siri": "http://www.siri.org.uk/siri"}
LIGNES_METRO = {"ILEVIA:Line::M1:LOC", "ILEVIA:Line::RME1:LOC"}

CHEMIN_CSV = Path("data/collecte/m1_rme1_siri.csv")
COLONNES = [
    "horodatage_collecte",
    "line_ref",
    "item_identifier",
    "monitoring_ref",
    "recorded_at_time",
    "expected_departure_time",
    "departure_status",
    "direction_name",
]


def extraire_texte(element, chemin):
    """Renvoie le texte d'un sous-element XML, ou None s'il est absent.
    Evite de repeter la meme verification 'is not None' partout."""
    trouve = element.find(chemin, ns)
    return trouve.text if trouve is not None else None


def collecter_une_fois():
    horodatage_collecte = datetime.now(timezone.utc).isoformat()

    reponse = requests.get(URL_SIRI, timeout=60)
    reponse.raise_for_status()
    racine = ET.fromstring(reponse.content)

    lignes_extraites = []
    for visite in racine.findall(".//siri:MonitoredStopVisit", ns):
        line_ref = extraire_texte(visite, ".//siri:LineRef")
        if line_ref not in LIGNES_METRO:
            continue

        lignes_extraites.append({
            "horodatage_collecte": horodatage_collecte,
            "line_ref": line_ref,
            "item_identifier": extraire_texte(visite, ".//siri:ItemIdentifier"),
            "monitoring_ref": extraire_texte(visite, ".//siri:MonitoringRef"),
            "recorded_at_time": extraire_texte(visite, ".//siri:RecordedAtTime"),
            "expected_departure_time": extraire_texte(visite, ".//siri:ExpectedDepartureTime"),
            "departure_status": extraire_texte(visite, ".//siri:DepartureStatus"),
            "direction_name": extraire_texte(visite, ".//siri:DirectionName"),
        })

    return lignes_extraites


def ajouter_au_csv(lignes):
    CHEMIN_CSV.parent.mkdir(parents=True, exist_ok=True)
    fichier_existe_deja = CHEMIN_CSV.exists()

    with open(CHEMIN_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLONNES)
        if not fichier_existe_deja:
            writer.writeheader()
        writer.writerows(lignes)


if __name__ == "__main__":
    lignes = collecter_une_fois()
    ajouter_au_csv(lignes)
    print(f"{len(lignes)} lignes M1/RME1 ajoutees a {CHEMIN_CSV}")