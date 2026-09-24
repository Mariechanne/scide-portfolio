"""
Verification retrospective : les 16 et 17 septembre 2026 etaient-ils
des jours de service "normaux" pour la ligne 1, en nombre de courses
reellement programmees, pas seulement en nombre de service_id actifs ?
"""

import pandas as pd
from pathlib import Path

ARCHIVE_DIR = Path("data/raw/gtfs_static_archive_20260916")

trips = pd.read_csv(ARCHIVE_DIR / "trips.txt")
calendar_dates = pd.read_csv(ARCHIVE_DIR / "calendar_dates.txt")

trips_me1 = trips[trips["route_id"] == "ME1"]
service_ids_me1 = trips_me1["service_id"].unique()

# Nombre de courses par service_id, pour ponderer correctement
# le nombre de service_id actifs par leur "poids" reel en courses.
nb_courses_par_service = trips_me1["service_id"].value_counts()

cal_me1 = calendar_dates[calendar_dates["service_id"].isin(service_ids_me1)]

for date in [20260916, 20260917, 20260923]:
    services_actifs_ce_jour = cal_me1[cal_me1["date"] == date]["service_id"]
    total_courses = sum(nb_courses_par_service.get(sid, 0) for sid in services_actifs_ce_jour)
    print(f"Date {date} : {len(services_actifs_ce_jour)} service_id actifs, "
          f"{total_courses} courses ME1 programmees au total")