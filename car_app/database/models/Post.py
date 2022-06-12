from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import INTEGER, Numeric
import car_app.database.DBManager as dbm 
import car_app.database.models.User as us 
import car_app.database.models.Country as ct
from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey, Numeric, DECIMAL
from sqlalchemy.orm import relationship
from datetime import datetime


class Post(dbm.DBManager.base()):
    __tablename__="information"
    RELATIVE_PHOTO_DIR="images"
    
    id = Column('id', Integer, autoincrement=True, primary_key=True)
    title = Column('title', String, nullable=False)
    brand = Column('brand', Text, nullable=False)
    model = Column('model', Text, nullable=False)
    price = Column('price', DECIMAL, nullable=False)
    year_made = Column('year_made', Numeric, nullable=False)
    mileage_km = Column('mileage_km', Integer, nullable=False)
    car_body = Column('car_body', Text, nullable=False)
    feul = Column('feul', Text, nullable=False)
    cubic = Column('cubic', Integer, nullable=False)
    engine_power_hp = Column('engine_power_hp', Integer, nullable=False)
    posted = Column('posted', Date, default=datetime.today)
    photo1 = Column('photo1', String, nullable=False)
    photo2 = Column('photo2', String, nullable=False)
    photo3 = Column('photo3', String, nullable=False)
    photo4 = Column('photo4', String, nullable=False)
    photo5 = Column('photo5', String, nullable=False)
    transmission = Column('transmission', Text, default="")
    original_color = Column('original_color', Text, default="")
    climate = Column('climate', Text, default="")
    doors = Column('doors', Integer, default="")
    user_id = Column(Integer, ForeignKey('users.id'))
    country_id = Column(Integer, ForeignKey('countries.id'))

    user = relationship("User", lazy="subquery")
    country = relationship("Country", lazy="subquery")
    
    
    @staticmethod
    def to_dict(post):
        return {
            "id": post.id, 
            "title": post.title, 
            "brand": post.brand,
            "model": post.model,
            "price": post.price,
            "year_made": post.year_made,
            "mileage_km": post.mileage_km,
            "car_body": post.car_body,
            "feul": post.feul,
            "cubic": post.cubic,
            "engine_power_hp": post.engine_power_hp,
            "posted": post.posted,
            "photo1": post.photo1,
            "photo2": post.photo2,
            "photo3": post.photo3,
            "photo4": post.photo4,
            "photo5": post.photo5,
            "transmission": post.transmission,
            "original_color": post.original_color,
            "climate": post.climate,
            "doors": post.doors,
            "user": us.User.to_dict(post.user),
            "country": ct.Country.to_dict(post.country)
        }