import os
import pyodbc
import azure.functions as func
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # Azure SQL Database configurations
        server = 'tcp:serverdiego09.database.windows.net,1433'
        database = 'db_diego'
        username = 'diego'
        password = 'edb4qempi..'
        driver = '{ODBC Driver 18 for SQL Server}'

        # Set up connection string
        conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'

        # Parse incoming JSON data
        data = req.get_json()

        # Connect to Azure SQL Database
        with pyodbc.connect(conn_str) as conn:
            with conn.cursor() as cursor:
                # Insert data into the database
                sql = "SELECT * FROM dbo.Persons"
                cursor.execute(sql)
                rows = cursor.fetchall()

                # Convert the result to a list of dictionaries
                result = [{'sensor': row.ID, 'value': row.LastName, 'firstname': row.FirstName, 'age': row.Age} for row in rows]

        return func.HttpResponse(json.dumps(result), mimetype='application/json', status_code=200)

    except Exception as e:
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)