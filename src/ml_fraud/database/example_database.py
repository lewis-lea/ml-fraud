import duckdb
import pathlib
from pathlib import Path
import requests
import ml_fraud

DEFAULT_DATA_PATH = ml_fraud.PROJECT_ROOT / "data"
TRANSACTIONS_SCHEMA_PATH = Path(__file__).parent / "transactions_schema.sql"
ACCOUNTS_SCHEMA_PATH = Path(__file__).parent / "accounts_schema.sql"


# Connects to the example raw database
# fetching it if required
def setup_example_database(
    data_folder_path: Path = DEFAULT_DATA_PATH,
) -> duckdb.DuckDBPyConnection:

    db_path: Path = data_folder_path / "db" / "SynSEPA.db"

    if not db_path.exists():
        print("Database does not exist, building it now")
        db_path.parent.mkdir(parents=True, exist_ok=True)
        db = build_database(data_folder_path)
    else:
        db = duckdb.connect(db_path, read_only=False)
    return db


# This function downloads and sets up the raw data databases
def build_database(data_path: Path = DEFAULT_DATA_PATH) -> duckdb.DuckDBPyConnection:

    # Set up data directory structure given
    # root folder
    transactions_csv = data_path / "raw" / "transactions.csv"
    accounts_csv = data_path / "raw" / "accounts.csv"
    db_path = data_path / "db" / "SynSEPA.db"

    # Rebuild the whole database everytime this function is run
    # because it is quick
    db_path.unlink(missing_ok=True)

    # If the data does not exist, we can fetch it from the source and store it in the raw data folder

    if not transactions_csv.exists():
        print("Fetching transactions data from source")
        response = requests.get(
            "http://huggingface.co/datasets/EpiphanyTech/SynSEPA/resolve/main/data/synsep_full_dataset.csv"
        )

        with open(transactions_csv, "wb") as f:
            f.write(response.content)
        print("Transactions data fetched and stored in", transactions_csv)

    else:
        print("Transactions data already exists in", transactions_csv)

    if not accounts_csv.exists():
        print("Fetching accounts data from source")
        response = requests.get(
            "https://huggingface.co/datasets/EpiphanyTech/SynSEPA/raw/main/data/accounts.csv"
        )
        with open(accounts_csv, "wb") as f:
            f.write(response.content)
            print("Accounts data fetched and stored in", accounts_csv)
    else:
        print("Accounts data already exists in", accounts_csv)

    # As ingestion cleaning is developed - it may be folded in here to simulate
    # cleaning done on entry to a production db

    db = duckdb.connect(db_path, read_only=False)
    db.execute(TRANSACTIONS_SCHEMA_PATH.read_text())
    db.execute(f"""
                    INSERT INTO transactions
                    SELECT *
                    FROM read_csv_auto('{transactions_csv}')
                """)

    # Create accounts using schema file then read in
    # the data
    db.execute(ACCOUNTS_SCHEMA_PATH.read_text())
    db.execute(f"""
                    INSERT INTO accounts
                    SELECT *
                    FROM read_csv_auto('{accounts_csv}')
                """)

    print("Database built at", db_path)
    return db
