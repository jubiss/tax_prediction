import pandas as pd

class get_data():
    """"
    Class constructor to retrieve data from SQL Databases and saves in the raw data folders.
    """
    def __init__(self, database):
        """
        Inform the type of database, allowed databases 'mysql'

        parameters:
        database: str
        """
        self.database = database
        return self
    
    def read_data(self, credentials, query, get_column_names=False, table_name=None):
        if self.database == 'mysql':
            import mysql.connector
            # Create a connection to the database
            #example of parameters
            """cnx = mysql.connector.connect(
                host='interview-2.ck1h5ksgzpiq.us-east-1.rds.amazonaws.com',
                port=3306,
                user='hotinterview',
                password='6cT4jk9QWPhQC9KXWKDd',
                database='innodb'
            )"""
            cnx = mysql.connector.connect(
                host=credentials['host'],
                port=credentials['port'],
                user=credentials['user'],
                password=credentials['password'],
                database=credentials['database']
            )

            # Create a cursor object to interact with the database
            cursor = cnx.cursor()

            if get_column_names:
                # Execute a sample query to get the column names
                query = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}'"
                cursor.execute(query)

                # Fetch all column names from the result
                columns = [column[0] for column in cursor.fetchall()]

                # Execute a query to fetch the table data
                query = f"SELECT * FROM {table_name}"
                cursor.execute(query)

            # Fetch all rows from the result
            rows = cursor.fetchall()

            # Transform in Dataframe
            df = pd.DataFrame(rows, columns=columns)
            # Save table data to a CSV file

            if table_name:
                df.to_csv(r'\data\raw\{table_name}.csv')
            else:
                df.to_csv(r'\data\raw\table.csv')
            # Close the cursor and connection
            cursor.close()
            cnx.close()

if __name__ == "__main__":
    database = 'mysql'
    credentials = {'host': None,
                   'port': None,
                   'user': None,
                   'password': None,
                   'database': None}
    query = " "
    get_column_names=False
    table_name = None
    data = get_data(database=database)
    data.read_data(credentials=credentials, query=query, get_column_names=get_column_names, table_name=table_name)