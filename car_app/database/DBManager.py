import sqlalchemy
from sqlalchemy.orm import declarative_base, Session, DeclarativeMeta
import car_app.database.DBEngine as dbe

class DBManager:
    METADATA = None
    SESSION = None 
    BASE = None 
    
    @classmethod
    def metadata(cls):
        if cls.METADATA == None:
            cls.METADATA = sqlalchemy.MetaData()
        return cls.METADATA
    
    @classmethod
    def base(cls) -> DeclarativeMeta:
        if cls.BASE == None:
            cls.BASE = declarative_base()
        return cls.BASE
    
    @classmethod
    def session(cls, echo=True, future=True) -> Session:
        connection = dbe.DBEngine.connect(echo, future)
        if cls.SESSION == None or \
            (cls.SESSION != None and not cls.SESSION.is_active):
                cls.SESSION = Session(connection)
        return cls.SESSION