"""
Etape 1 - Audit structurel du referentiel GTFS statique (ligne 1, ME1)

Objectif : verifier empiriquement, sur les fichiers reellement telecharges,
que la structure correspond a ce qu'on attend, avant toute jointure ou
tout nettoyage. Aucune transformation ici, uniquement de la lecture et
de l'observation.
"""

import pandas as pd
from pathlib import Path

# Chemin relatif vers les fichiers GTFS statique
GTFS_DIR = Path("data/raw/gtfs_static")

# --- Chargement des deux fichiers necessaires pour identifier la ligne 1 ---
routes = pd.read_csv(GTFS_DIR / "routes.txt")
trips = pd.read_csv(GTFS_DIR / "trips.txt")

# --- Verification de l'identifiant de la ligne 1 ---
# Le document de cadrage suppose route_id == "ME1", mais on le verifie
# sur les donnees reelles plutot que de le tenir pour acquis.
print("Lignes disponibles dans routes.txt :")
print(routes[["route_id", "route_short_name", "route_long_name"]])

# --- Filtrage des courses theoriques de la ligne 1 ---
trips_me1 = trips[trips["route_id"] == "ME1"]
print(f"\nNombre de courses theoriques ME1 : {len(trips_me1)}")

# --- Apercu du calendrier associe a ces courses ---
# Utile pour anticiper l'etape suivante, ou on confrontera ceci
# au contenu (volumineux) de calendar_dates.txt
print("\nRepartition des courses ME1 par service_id :")
print(trips_me1["service_id"].value_counts())


# --- Etape 2 (amorce) : structure du calendrier associe a ME1 ---
# On verifie l'hypothese : calendar.txt est-il vraiment absent,
# et calendar_dates.txt declare-t-il un jour de service par ligne ?

calendar_dates = pd.read_csv(GTFS_DIR / "calendar_dates.txt")

service_ids_me1 = trips_me1["service_id"].unique()
print(f"\nNombre de service_id distincts pour ME1 : {len(service_ids_me1)}")

print(f"\nColonnes de calendar_dates.txt : {calendar_dates.columns.tolist()}")
print(f"Valeurs uniques de exception_type : {calendar_dates['exception_type'].unique()}")

# On isole les lignes de calendar_dates qui concernent un service_id de ME1
cal_me1 = calendar_dates[calendar_dates["service_id"].isin(service_ids_me1)]
print(f"\nNombre de lignes calendar_dates concernant ME1 : {len(cal_me1)}")
print(f"Periode couverte : du {cal_me1['date'].min()} au {cal_me1['date'].max()}")