import car_app.database.DBManager as dbm 
from sqlalchemy import Column, Integer, String


class User(dbm.DBManager.base()):
    __tablename__="users"

    id = Column('id', Integer, autoincrement=True, primary_key=True)
    username = Column('username', String, nullable=False, unique=True) 
    email = Column('email', String, nullable=False, unique=True)
    password = Column('password', String, nullable=False)


    @staticmethod
    def to_dict(user)->dict:
        return {
            "id": user.id,
            "username": user.username, 
            "email": user.email,
        }