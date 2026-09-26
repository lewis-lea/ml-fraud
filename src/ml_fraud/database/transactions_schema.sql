CREATE TABLE IF NOT EXISTS transactions
(
transaction_id                  VARCHAR,
account_id                      VARCHAR,
persona                         VARCHAR,
timestamp                       TIMESTAMP,
sender_iban                     VARCHAR,
beneficiary_iban                VARCHAR,
beneficiary_country             VARCHAR,
country_type                    VARCHAR,
amount                          DOUBLE,
remittance_category             VARCHAR,
remittance_text                 VARCHAR,
hour_of_day                     UTINYINT,
day_of_week                     UTINYINT,
is_weekend                      BOOLEAN NOT NULL,
time_since_last_txn             DOUBLE,
is_new_beneficiary              BOOLEAN NOT NULL,
is_fraud                        BOOLEAN NOT NULL,
fraud_type                      VARCHAR
);