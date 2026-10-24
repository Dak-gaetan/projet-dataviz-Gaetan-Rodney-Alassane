-- Exécuté une seule fois à la création du volume PostgreSQL.
-- Les tables gold sont (ré)écrites par le notebook 02_silver_gold.ipynb.

CREATE SCHEMA IF NOT EXISTS gold;

-- Exemple de structure : à adapter à la question du persona
-- CREATE TABLE IF NOT EXISTS gold.penurie_par_station_heure (
--   station_id    TEXT NOT NULL,
--   heure         SMALLINT NOT NULL,
--   jour_semaine  SMALLINT NOT NULL,
--   taux_penurie  DOUBLE PRECISION,
--   taux_saturation DOUBLE PRECISION,
--   PRIMARY KEY (station_id, heure, jour_semaine)
-- );
