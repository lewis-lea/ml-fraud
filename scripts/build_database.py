import duckdb
import pathlib
import requests

# This script exists to convet the pandas dataframes into a duckdb database
# to simulate downstram learning from a more realistic data source

# Rebuild the whole database everyt time this script is run
# because it is quick
pathlib.Path("data/db/SynSEPA.duckdb").unlink(missing_ok=True)

# If the data does not exist, we can fetch it from the source and store it in the raw data folder
if not pathlib.Path("data/raw/transactions.csv").exists():
   print("Fetching transactions data from source")
   response = requests.get("http://huggingface.co/datasets/EpiphanyTech/SynSEPA/resolve/main/data/synsep_full_dataset.csv")
   with open("data/raw/transactions.csv", "wb") as f:
       f.write(response.content)
   print("Transactions data fetched and stored in data/raw/transactions.csv")
else:
    print("Transactions data already exists in data/raw/transactions.csv")

if not pathlib.Path("data/raw/accounts.csv").exists():
   print("Fetching accounts data from source")
   response = requests.get("https://huggingface.co/datasets/EpiphanyTech/SynSEPA/raw/main/data/accounts.csv")
   with open("data/raw/accounts.csv", "wb") as f:
       f.write(response.content)
   print("Accounts data fetched and stored in data/raw/accounts.csv")
else:
    print("Accounts data already exists in data/raw/accounts.csv")

# As ingestion cleaning is developed - it may be folded in here to simulate
# cleaning done on entry to a production db

# transactionData = pandas.read_csv("data/raw/SynSEPA.csv")
# accountData = pandas.read_csv("data/raw/accounts.csv")

db = duckdb.connect("data/db/SynSEPA.duckdb", read_only=False)
db.execute("""
                CREATE TABLE transactions AS
                SELECT *
                FROM read_csv_auto('data/raw/transactions.csv')
            """)
db.execute("""
                CREATE TABLE accounts AS
                SELECT *
                FROM read_csv_auto('data/raw/accounts.csv')
            """)

print("Database built at data/db/SynSEPA.duckdb")