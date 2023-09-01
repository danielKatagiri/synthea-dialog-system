CREATE DATABASE synthea;
\c synthea;

-- Config for the DB to accept pt-br words
update pg_database set encoding = pg_char_to_encoding('UTF8') where datname = 'synthea';

CREATE TABLE patient (
  patient_id uuid NOT NULL,
  active BOOLEAN,
  given_name VARCHAR,
  family_name VARCHAR,
  telecom VARCHAR,
  gender VARCHAR,
  birth_date TIMESTAMP,
  deceased_boolean BOOLEAN,
  deceased_datetime TIMESTAMP,
  address VARCHAR,
  marital_status VARCHAR,
  language VARCHAR,
  PRIMARY KEY (patient_id)
);

CREATE TABLE condition (
  condition_id UUID NOT NULL,
  name VARCHAR,
  clinical_status VARCHAR,
  category VARCHAR,
  subject UUID,
  onset_datetime TIMESTAMP,
  abatement_datetime TIMESTAMP,
  recorded_date TIMESTAMP,
  PRIMARY KEY (condition_id),
  FOREIGN KEY (subject) REFERENCES patient(patient_id)
);
