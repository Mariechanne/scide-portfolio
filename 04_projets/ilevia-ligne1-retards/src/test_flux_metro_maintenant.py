"""
Test decisif : en interrogeant le flux SIRI maintenant, en direct,
les entrees M1/RME1 montrent-elles encore les memes identifiants et
horaires figes depuis le 18-20 septembre, ou de nouvelles entrees
sont-elles enfin apparues ?
"""

import xml.etree.ElementTree as ET
import requests

URL_SIRI = "https://proxy.transport.data.gouv.fr/resource/ilevia-lille-siri-sm"
ns = {"siri": "http://www.siri.org.uk/siri"}
lignes_metro = {"ILEVIA:Line::M1:LOC", "ILEVIA:Line::RME1:LOC"}

reponse = requests.get(URL_SIRI, timeout=60)
reponse.raise_for_status()
racine = ET.fromstring(reponse.content)

print("Entrees M1/RME1 dans le flux EN DIRECT, maintenant :\n")
for v in racine.findall(".//siri:MonitoredStopVisit", ns):
    line_ref = v.find(".//siri:LineRef", ns)
    if line_ref is None or line_ref.text not in lignes_metro:
        continue
    item_id = v.find(".//siri:ItemIdentifier", ns)
    recorded = v.find(".//siri:RecordedAtTime", ns)
    expected = v.find(".//siri:ExpectedDepartureTime", ns)
    print(f"- {item_id.text if item_id is not None else '?'} | "
          f"enregistre le : {recorded.text if recorded is not None else '?'} | "
          f"depart prevu : {expected.text if expected is not None else '?'}")