"""
Vue d'ensemble sur TOUS les enregistrements M1 et RME1 du flux SIRI,
pas un seul exemple : verifie l'hypothese ALLER/RETOUR sur l'ensemble,
et repere la presence ou l'absence d'un champ d'horaire theorique
(AimedDepartureTime) selon le statut du depart.
"""

import xml.etree.ElementTree as ET
import requests

URL_SIRI = "https://proxy.transport.data.gouv.fr/resource/ilevia-lille-siri-sm"
ns = {"siri": "http://www.siri.org.uk/siri"}

reponse = requests.get(URL_SIRI, timeout=60)
reponse.raise_for_status()
racine = ET.fromstring(reponse.content)
visites = racine.findall(".//siri:MonitoredStopVisit", ns)

lignes_metro = {"ILEVIA:Line::M1:LOC", "ILEVIA:Line::RME1:LOC"}

print(f"{'LineRef':<25} {'DirectionName':<10} {'DepartureStatus':<12} {'AimedDepartureTime present ?'}")
for v in visites:
    line_ref = v.find(".//siri:LineRef", ns)
    if line_ref is None or line_ref.text not in lignes_metro:
        continue

    direction = v.find(".//siri:DirectionName", ns)
    statut = v.find(".//siri:DepartureStatus", ns)
    aimed = v.find(".//siri:AimedDepartureTime", ns)

    print(f"{line_ref.text:<25} "
          f"{(direction.text if direction is not None else '?'):<10} "
          f"{(statut.text if statut is not None else '?'):<12} "
          f"{'Oui' if aimed is not None else 'Non'}")