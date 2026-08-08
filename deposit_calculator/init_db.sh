#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
CREATE TABLE IF NOT EXISTS deposits (
    id SERIAL PRIMARY KEY,
    date VARCHAR(255),
    periods INTEGER,
    amount INTEGER,
    rate FLOAT
);
EOSQL