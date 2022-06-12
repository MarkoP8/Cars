import os
import configparser
import sqlalchemy
from car_app.database.exceptions.SettingsFileNotExistException import SettingsFileNotExistException
from car_app.database.exceptions.NoDatabaseSettingsException import NoDatabaseSettingsException
from car_app.database.exceptions.NoRequiredOptionException import NoRequiredOptionException
class DBEngine:
    SETTINGS_FILE = ""
    ENGINE = None 
    
    @staticmethod
    def set_settings_path(file_path: str, is_absolute: bool=False):
        if is_absolute == True:
            DBEngine.SETTINGS_FILE = file_path
        else:
            dir_path = os.path.dirname(os.path.abspath(__file__))
            DBEngine.SETTINGS_FILE = \
            os.path.join(dir_path, file_path)
    
    @staticmethod
    def load_configuration() -> configparser.ConfigParser:
        if not os.path.exists(DBEngine.SETTINGS_FILE):
            raise SettingsFileNotExistException(DBEngine.SETTINGS_FILE)
        parser = configparser.ConfigParser()
        parser.read(DBEngine.SETTINGS_FILE)
        
        if not parser.has_section("database"):
            raise NoDatabaseSettingsException() 
        
        if not parser.has_option("database", "host"):
            raise NoRequiredOptionException("host")
        if not parser.has_option("database", "db_name"):
            raise NoRequiredOptionException("db_name")
        
        return parser
    
    @staticmethod
    def create_connection_string():
        connection_string = "mysql+mysqlconnector://"
        parser = DBEngine.load_configuration()
        
        if parser.has_option("database", "user"):
            connection_string += parser['database']['user']
            if parser.has_option("database", "password"):
                connection_string += ":" + parser['database']['password']
            connection_string += "@"
            
        connection_string += parser['database']['host']
        if parser.has_option("database", "port"):
            connection_string += ":" + parser['database']['port']
        
        connection_string += "/" + parser['database']['db_name']
            
        if parser.has_option("database", "charset"):
            connection_string += "?charset=" + parser['database']['charset']
            
        return connection_string
    
    @staticmethod
    def connect(echo:bool=True, future:bool=True) -> sqlalchemy.engine.Connection:
        if DBEngine.ENGINE == None:
            connection_string = DBEngine.create_connection_string()
            DBEngine.ENGINE = sqlalchemy.create_engine(connection_string, echo=echo, future=future)
        return DBEngine.ENGINE.connect()
    
    @staticmethod
    def get(echo:bool=True, future:bool=True) -> sqlalchemy.engine.Engine:
        if DBEngine.ENGINE == None:
            connection_string = DBEngine.create_connection_string()
            DBEngine.ENGINE = sqlalchemy.create_engine(connection_string, echo=echo, future=future)
        return DBEngine.ENGINE