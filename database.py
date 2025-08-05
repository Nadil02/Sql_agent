from langchain_community.utilities import SQLDatabase

server = "nadilsqlagent.database.windows.net"
database = "AdventureWorks2019"
username = "sqladmin"
password = "1Aaaaaaaa"

db_uri = f"mssql+pyodbc://{username}:{password}@{server}/{database}?driver=ODBC Driver 17 for SQL Server"

db = SQLDatabase.from_uri(db_uri, schema="Person")
print("tables:", db.get_usable_table_names())
