# =====================================================================
# COLLECTE DES PERTURBATIONS MEL (journal des changements)
# =====================================================================
# Interroge le service des perturbations une fois, et ajoute au CSV
# uniquement les entrees nouvelles ou modifiees depuis le dernier passage.
# Usage : python src/collecte_perturbations_mel.py
# (a lancer depuis 04_projets/ilevia-ligne1-retards)

import csv
from datetime import datetime, timezone
from pathlib import Path

import requests

# ---------------------------------------------------------------------
# Parametres
# ---------------------------------------------------------------------
URL = ("https://data.lillemetropole.fr/geoserver/ogc/features/v1/"
       "collections/dsp_ilevia:perturbations/items")
CHEMIN_CSV = Path("data/collecte/perturbations_mel.csv")
CIBLES_METRO = {"ILEVIA:LineRef::ME1:LOC", "ILEVIA:LineRef::ME2:LOC", "Global"}

# Une entree est "deja vue" si ces trois valeurs existent deja dans le CSV
CLE = ("identifiant_perturbation", "identifiant_message", "date_modification")

COLONNES = [
    "horodatage_collecte",   # quand CE script a interroge le flux (UTC)
    "horodatage_flux",       # l'horodatage annonce par le flux (UTC)
    "objectid",
    "identifiant_perturbation",
    "identifiant_message",
    "type_perturbation",
    "cible",
    "message",
    "date_modification",     # attention : heure de Paris etiquetee "Z"
    "heure_fin_prevue",      # idem
]


# ---------------------------------------------------------------------
# Fonctions
# ---------------------------------------------------------------------
def telecharger():
    reponse = requests.get(URL, params={"limit": 1000}, timeout=60)
    reponse.raise_for_status()
    return reponse.json()


def a_garder(proprietes):
    return (proprietes.get("type_perturbation") == "Perturbation"
            or proprietes.get("cible") in CIBLES_METRO)


def cle_de(proprietes):
    # str(... or "") : une valeur absente et une cellule vide du CSV
    # donnent la meme cle, sinon on ajouterait des doublons.
    return tuple(str(proprietes.get(c) or "") for c in CLE)


def cles_deja_vues():
    if not CHEMIN_CSV.exists():
        return set()
    with open(CHEMIN_CSV, newline="", encoding="utf-8") as f:
        return {tuple(ligne[c] for c in CLE) for ligne in csv.DictReader(f)}


# ---------------------------------------------------------------------
# Programme principal
# ---------------------------------------------------------------------
if __name__ == "__main__":
    donnees = telecharger()
    horodatage_collecte = datetime.now(timezone.utc).isoformat()
    horodatage_flux = donnees.get("timeStamp")

    vues = cles_deja_vues()
    nouvelles = []
    for entree in donnees.get("features", []):
        p = entree["properties"]
        if not a_garder(p):
            continue
        cle = cle_de(p)
        if cle in vues:
            continue
        vues.add(cle)
        ligne = {"horodatage_collecte": horodatage_collecte,
                 "horodatage_flux": horodatage_flux}
        ligne.update({c: p.get(c) for c in COLONNES[2:]})
        nouvelles.append(ligne)

    CHEMIN_CSV.parent.mkdir(parents=True, exist_ok=True)
    nouveau_fichier = not CHEMIN_CSV.exists()
    with open(CHEMIN_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLONNES)
        if nouveau_fichier:
            writer.writeheader()
        writer.writerows(nouvelles)

    print(f"{len(donnees.get('features', []))} entrees dans le flux, "
          f"{len(nouvelles)} nouvelles ajoutees a {CHEMIN_CSV}")