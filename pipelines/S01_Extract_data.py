import pandas as pd
import pyodbc
import logging
import keyring as kr
import warnings

warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(filename='pipelines/etl_pipeline_log.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class DatabaseCredentials:

    def __init__(self, server: str, database: str) -> None:
        self.server = server
        self.database = database

    def get_credentials(self) -> tuple:
        username = kr.get_password("sql_server", "username")
        password = kr.get_password("sql_server", "password")
        return username, password

class ETLProcess:

    def __init__(self, db_credentials: DatabaseCredentials) -> None:
        self.db_credentials = db_credentials



    # def create_database(self) -> None:
    #     try:
    #         # Establish a connection to the master database to create the target database
    #         cnxn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={self.db_credentials.server};'
    #                               f'DATABASE=master;Trusted_Connection=yes;')
    #         cursor = cnxn.cursor()

    #         # Create the database if it doesn't exist
    #         query = f"""
    #                     IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'ETL')
    #                     BEGIN
    #                         CREATE DATABASE ETL
    #                     END
    #                 """
                    
    #         cursor.execute(query)
    #         cnxn.commit()

    #         print(f"Database created successfully.")

        # except Exception as e:
        #     logging.error(f"Database creation error: {e}")
        #     print(f"Database creation error: {e}")
        # finally:
        #     cnxn.close()

    def extract(self) -> pd.DataFrame:
        try:
            # Get database credentials from keyring (Currently not used)
            username, password = self.db_credentials.get_credentials()

            # Establish a connection to the SQL Server database
            cnxn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={self.db_credentials.server};'
                                  f'DATABASE={self.db_credentials.database};Trusted_Connection=yes;')
            cursor = cnxn.cursor()

            # Retrieve data from the database
            query = """SELECT * FROM AdventureWorks2019.Person.Person"""
            df = pd.read_sql(query, cnxn)

            print(f"Data extracted successfully; Data Shape:{df.shape} ")
            return df

        except Exception as e:
            logging.error(f"Data extract error: {e}")
            print(f"Data extract error: {e}")
            return None
        finally:
            cnxn.close()

    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        try:
            # Add transformation logic here
            data['NewColumn'] = 'Transformation Dummy'
            print(f"Data transformed successfully; Data Shape {data.shape}")
            return data

        except Exception as e:
            logging.error(f"Data transform error: {e}")
            print(f"Data transform error: {e}")
            return None

    def load(self, data: pd.DataFrame, target_table: str) -> None:
        try:
            # Establish a connection to the target SQL Server database (ETL database)
            cnxn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={self.db_credentials.server};'
                                  f'DATABASE=ETL;Trusted_Connection=yes;')
            # cursor = cnxn.cursor()

            # # Create the target table if it doesn't exist
            # create_table_query = f"""
            # IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES 
            #                WHERE TABLE_SCHEMA = 'dbo' AND TABLE_NAME = 'ETL_Table')
            # BEGIN
            #     CREATE TABLE ETL_Table (
            #         BusinessEntityID INT PRIMARY KEY,
            #         PersonType NVARCHAR(50),
            #         NameStyle BIT,
            #         Title NVARCHAR(50),
            #         FirstName NVARCHAR(50),
            #         MiddleName NVARCHAR(50),
            #         LastName NVARCHAR(50),
            #         Suffix NVARCHAR(50),
            #         EmailPromotion INT,
            #         AdditionalContactInfo XML,
            #         Demographics XML,
            #         rowguid UNIQUEIDENTIFIER,
            #         ModifiedDate DATETIME,
            #         NewColumn NVARCHAR(50)
            #     );
            # END
            # """
            # cursor.execute(create_table_query)
            # cnxn.commit()

            # Insert data into the target table
            data.to_sql(name=target_table, con=cnxn, index=False, if_exists='append')

            print("Data loaded successfully")

        except Exception as e:
            logging.error(f"Data load error: {e}")
            print(f"Data load error: {e}")
        finally:
            cnxn.close()

if __name__ == "__main__":
    try:
        db_credentials = DatabaseCredentials(server='PRECISION\\SQLEXPRESS', database='AdventureWorks2019')
        etl_process = ETLProcess(db_credentials)
        # etl_process.create_database()
        
        extracted_data = etl_process.extract()

        if extracted_data is not None:
            transformed_data = etl_process.transform(extracted_data)
            if transformed_data is not None:
                etl_process.load(transformed_data, target_table='ETL_Table')

    except Exception as e:
        logging.error(f"Error occurred: {e}")
        print(f"Error occurred: {e}")















#old
# import pandas as pd
# import pyodbc
# import logging
# import keyring as kr
# import warnings

# warnings.filterwarnings('ignore')


# # Configure logging to both a file and the console
# logging.basicConfig(filename='pipelines/etl_pipeline_log.log', level=logging.INFO,
#                     format='%(asctime)s - %(levelname)s - %(message)s')

# class DatabaseCredentials:

#     def __init__(self, server: str, database: str) -> None:
#         self.server = server
#         self.database = database

#     def get_credentials(self) -> tuple:

#         username = kr.get_password("sql_server", "username")
#         password = kr.get_password("sql_server", "password")
#         return username, password

# class ETLProcess:

#     def __init__(self, db_credentials: DatabaseCredentials) -> None:
#         self.db_credentials = db_credentials

#     def extract(self) -> None:

#         try:
#             # Get database credentials from keyring, Currently not used**
#             username, password = self.db_credentials.get_credentials()

#             # Establish a connection to the SQL Server database
#             cnxn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={self.db_credentials.server};'
#                                   f'DATABASE={self.db_credentials.database};Trusted_Connection=yes;')
#             cursor = cnxn.cursor()

#             # Retrieve table names from the database
#             query = """SELECT * FROM AdventureWorks2019.Person.Person"""

#             df = pd.read_sql(query, cnxn)

#             print(df.head())

#             return df

#         except Exception as e:
#             logging.error(f"Data extract error: {e}")
#         finally:
#             cnxn.close()


#     def transform(self, data: pd.DataFrame) -> pd.DataFrame:

#         try:

#             data['NewColumn'] = 'Transformation Dummy'

#             return data

#         except Exception as e:
#             logging.error(f"Data transform error: {e}")
#             return None
        
#     def load(self, data: pd.DataFrame, target_table: str) -> None:

#             try:
#                 # Establish a connection to the target SQL Server database (ETL database)
#                 cnxn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={self.db_credentials.server};'
#                                     f'DATABASE=ETL;Trusted_Connection=yes;')
#                 cursor = cnxn.cursor()

#                 # Create the target table if it doesn't exist
#                 create_table_query = f"""
#                         CREATE TABLE {target_table}
#                             (
#                                 BusinessEntityID INT PRIMARY KEY,
#                                 PersonType NVARCHAR(50),
#                                 NameStyle BIT,
#                                 Title NVARCHAR(50),
#                                 FirstName NVARCHAR(50),
#                                 MiddleName NVARCHAR(50),
#                                 LastName NVARCHAR(50),
#                                 Suffix NVARCHAR(50),
#                                 EmailPromotion INT,
#                                 AdditionalContactInfo XML, -- Assuming AdditionalContactInfo is stored as XML
#                                 Demographics XML, -- Assuming Demographics is stored as XML
#                                 rowguid UNIQUEIDENTIFIER,
#                                 ModifiedDate DATETIME,
#                                 NewColumn NVARCHAR(50)

#                             );
#                 """
#                 cursor.execute(create_table_query)
#                 cnxn.commit()

#                 # Insert data into the target table
#                 data.to_sql(name=target_table, con=cnxn, index=False, if_exists='append')

#                 print("Loaded")

#             except Exception as e:
#                 logging.error(f"Data load error: {e}")
#             finally:
#                 cnxn.close()

    

# if __name__ == "__main__":

#     try:

#         db_credentials = DatabaseCredentials(server='PRECISION\\SQLEXPRESS', database='AdventureWorks2019')
#         etl_process = ETLProcess(db_credentials)
#         extracted_data = etl_process.extract()

#         if extracted_data is not None:

#             transformed_data = etl_process.transform(extracted_data)
#             print(transformed_data.head(1).T)

#             etl_process.load(transformed_data, target_table='ETL_DataTable')


#     except Exception as e:
#         logging.error(f"Error occurred: {e}")