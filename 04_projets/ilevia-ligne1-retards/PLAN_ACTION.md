# Plan d'action - Analyse des retards de la ligne 1 (ilévia)

## 1. Question de recherche et objectifs

### Phase 0 (faisabilité, réalisée)

- Audit du référentiel GTFS statique : ME1 confirmé (route_id), ~8000 courses
  théoriques sur la période, calendrier encodé jour par jour (pas de
  calendar.txt).
- Vérification rétrospective via l'API de transport.data.gouv.fr (version
  archivée du 16/09/2026) : le calendrier théorique des 16 et 17 septembre
  2026 ne montre aucune dégradation par rapport à un jour ordinaire,
  écartant l'hypothèse de saisonnalité au niveau de la planification.
- Source temps réel identifiée : flux SIRI SM (le canal GTFS-RT trip_updates
  ne couvre pas le métro). Le métro y apparaît sous deux references (M1,
  RME1), nature encore à élucider ; absence constatée d'un champ d'horaire
  théorique (AimedDepartureTime) dans les exemples observés à ce jour.
- Capture brute du flux SIRI en place depuis le 24/09/2026 (tâche planifiée
  locale), à remplacer par une collecte continue sur GitHub Actions.
- Collecte continue autonome en place depuis le 02/10/2026 via GitHub Actions
  (toutes les 5 minutes, extraction ciblee M1/RME1 vers
  data/collecte/m1_rme1_siri.csv, commits attribues a l'identite Mariechanne).

### Phase 1 (explicative) : identifier si des variables mesurables (calendrier,
horaire, jour de semaine, éventuellement météo) sont statistiquement
associées à la survenue de perturbations sur la ligne 1, sur la fenêtre de
collecte disponible avant décembre 2026. Livrable pour début décembre 2026,
avant le début des candidatures de stage.

### Phase 2 (predictive) : une fois davantage de donnees accumulees (au-dela de
decembre), construire un modele capable d'anticiper une perturbation a
venir, reprise en arriere-plan sans contrainte de delai.

## 2. Revue de littérature

## 3. Données

## 4. Méthode

## 5. Calendrier

## 6. Limites anticipées

- Le flux SIRI SM ne transmet jamais de champ AimedDepartureTime (horaire
  theorique) dans les enregistrements observes a ce jour : le calcul d'un
  retard en minutes necessitera de croiser avec le referentiel GTFS statique
  via le trip ou l'arret, pas une simple comparaison interne au flux.
- Le statut "noReport" (tres majoritaire dans les observations) ne signifie
  pas "a l'heure" : il indique une absence d'information, pas une confirmation
  de ponctualite. Seul le statut "onTime" est un signal positif fiable a ce
  stade ; aucun retard reel n'a encore ete observe dans les donnees.
- Des entrees "figees" (recorded_at_time tres ancien par rapport a
  l'horodatage de collecte) existent specifiquement sur M1/RME1 (absentes
  sur une ligne de bus temoin) : un filtre de fraicheur sera necessaire avant
  toute analyse.
- La distinction entre les references M1 et RME1 n'est pas encore comprise
  (ce n'est pas le sens de circulation, confirme empiriquement) ; a
  documenter une fois davantage de donnees accumulees.
- Fenetre de collecte avec un trou : test dense du 24 au 26/09/2026 (tache
  planifiee locale, desactivee depuis), puis collecte continue reelle
  seulement a partir du 02/10/2026 (GitHub Actions). A assumer explicitement
  dans le README final, pas a presenter comme une collecte ininterrompue
  depuis le debut du projet.