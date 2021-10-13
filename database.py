from configuration import Configuration
from sqlalchemy import create_engine
from hashlib import sha256
import pandas as pd

class Database:
    # Create a private instance of the Configuration class that will be used to parse the .ini file
    __configuration = Configuration()
    
    # Define the queries which are used by the various methods for interacting witht the database
    __login_query = "SELECT id, username FROM user_profile WHERE username = '{0}' AND password = '{1}'"
    
    def __init__(self, filename='database.ini', section='postgresql'):        
        # Create a new instance of the engine for querying the underlying database
        self.__engine = create_engine(self.__configuration.parse(filename, section))
    
    def __execute_query(self, query):
        salted_hash = sha256
        return pd.read_sql(query, self.__engine)
    
    def __generate_hash(self, salt, text):
        return sha256(f"{salt}|{text}".encode()).hexdigest()
    
    def login(self, username, password):
        password_hash = self.__generate_hash(username, password)
        return self.__execute_query(self.__login_query.format(username, password_hash))
    
    def save(self, portfolio):
        #TODO: Implement the logic to persist to the database
        raise Exception("Not Implemented Yet")
