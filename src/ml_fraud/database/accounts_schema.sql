CREATE TABLE IF NOT EXISTS accounts
(
account_id                     VARCHAR,
persona                        VARCHAR,
description                    VARCHAR,
home_country                   VARCHAR,
sender_iban                    VARCHAR,
txn_per_month_min              BIGINT,
txn_per_month_max              BIGINT,
typical_amount                 DOUBLE,
foreign_txn_prob               DOUBLE,
weekend_factor                 DOUBLE,
fraud_target_types             VARCHAR,
known_beneficiaries            VARCHAR,
known_beneficiary_count        BIGINT
);