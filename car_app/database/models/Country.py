import car_app.database.DBManager as dbm 
from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey

class Country(dbm.DBManager.base()):
    __tablename__="countries"
    id = Column('id', Integer, autoincrement=True, primary_key=True)
    name = Column('name', String, nullable=False)
    
    @staticmethod
    def to_dict(country):
        return {
            "id": country.id, 
            "name": country.name
        }