import pandas as pd

class get_data():
    """"
    Class constructor to retrieve data from SQL Databases and saves in the raw data folders.
    """
    def __init__(self, credentials):
        """
        Inform the credentails and the database that will be used, allowed databases 'mysql'

        parameters:
        credentials: dict
        """
        self.credentials = credentials
    
    def save_data(self, query, get_column_names=False, table_name=None):
            cnx = self.get_connection()

            # Create a cursor object to interact with the database
            cursor = cnx.cursor()

            if get_column_names:
                columns = self.column_names(cursor=cursor, table_name=table_name)
                # Execute a query to fetch the table data
                query = f"SELECT {','.join(columns)} FROM {table_name}"
                cursor.execute(query)

            else:
                cursor.execute(query)
            # Fetch all rows from the result
            rows = cursor.fetchall()

            if credentials['charset'] != None:
                # Decode the column values
                decoded_rows = self.decode(rows)
                # Transform in Dataframe
                df = pd.DataFrame(decoded_rows, columns=columns)
            else:
                # Transform in Dataframe
                df = pd.DataFrame(rows, columns=columns)

            # Save table data to a CSV file
            if table_name == None:
                table_name = 'table'

            df.to_csv(fr'data\raw\{table_name}.csv', index=False)

            # Close the cursor and connection
            cursor.close()
            cnx.close()

    def get_connection(self):
        if self.credentials['database'] == 'mysql':
            import mysql.connector
            cnx = mysql.connector.connect(
                host=self.credentials['host'],
                port=self.credentials['port'],
                user=self.credentials['user'],
                password=self.credentials['password'],
                database=self.credentials['database_path'],
            )
        if self.credentials['database'] == 'fdb':
            import fdb
            cnx = fdb.connect(
                host=self.credentials['host'],
                port=self.credentials['port'],
                user=self.credentials['user'],
                password=self.credentials['password'],
                database=self.credentials['database_path'],
                charset=self.credentials['charset']
            )
        return cnx

    def decode(self, rows):
        if self.credentials['database'] == 'fdb':
            decoded_rows = []
            for row in rows:
                decoded_row = []
                for value in row:
                    if isinstance(value, bytes):
                        try:
                            decoded_value = value.decode(self.credentials['charset'])
                        except UnicodeDecodeError:
                            decoded_value = value.decode(self.credentials['charset'], errors='replace')
                        decoded_row.append(decoded_value)
                    else:
                        decoded_row.append(value)
                decoded_rows.append(decoded_row)
        return decoded_rows
    
    def column_names(self, cursor, table_name):
        # Execute a sample query to get the column names
        if self.credentials['database'] == 'mysql':
            query = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}'"
        if self.credentials['database'] == 'fdb':
            query = f"SELECT rdb$field_name FROM rdb$relation_fields WHERE rdb$relation_name = '{table_name}'"

        cursor.execute(query)

        # Fetch all column names from the result
        if (credentials['charset'] != None) and (credentials['database'] == 'fdb'):
            columns = [column[0].strip() for column in self.decode(cursor.fetchall())]
        else:
            columns = [column[0].strip() for column in cursor.fetchall()]
        return columns
    
if __name__ == "__main__":
    credentials = {'database': 'fdb',
                   'host': 'localhost',
                   'port': None,
                   'user': 'sysdba',
                   'password': 'masterkey',
                   'database_path': r'C:\Users\jubi\Desktop\Projetos\projetos proissionais\juliana_comercial_returns\data\BM.FDB',
                   'charset': 'ISO8859_1'}
    query = ""
    get_column_names=True
    table_names = ['PRODUTO', 'ENTRADA_PRODUTO', 'ENTRADA', 'PESSOA']
    data = get_data(credentials=credentials)
    for table_name in table_names:
        print(table_name)
        data.save_data(query=query, get_column_names=get_column_names, table_name=table_name)