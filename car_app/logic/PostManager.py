from sqlalchemy.sql.functions import current_user
import car_app.database.DBManager as dbm 
import car_app.database.models.Post as pt
import car_app.database.models.User as us
from datetime import datetime
from sqlalchemy import desc
import os

def save_image(file):
    if file.filename != "":
        file.save(os.path.join("car_app", "static", "cars_images", file.filename))
    return file.filename

class PostManager:
    
    @staticmethod
    def save_post(form_data, files, user_id):
        post = pt.Post()
        post.title = form_data['post_title']
        post.brand = form_data['post_brand']
        post.model = form_data['post_model']
        post.price = form_data['post_price']
        post.year_made = form_data['post_year_made']
        post.mileage_km = form_data['post_mileage_km']
        post.car_body = form_data['post_car_body']
        post.feul = form_data['post_feul']
        post.cubic = form_data['post_cubic']
        post.engine_power_hp = form_data['post_engine_power_hp']
        post.transmission = form_data['post_transmission']
        post.original_color = form_data['post_original_color']
        post.climate = form_data['post_climate']
        post.doors = form_data['post_doors']
        post.country_id = int(form_data['post_country'])
        post.user_id = user_id 
        post.posted = datetime.now()
        post.photo1 = save_image(files["file1"])
        post.photo2 = save_image(files["file2"])
        post.photo3 = save_image(files["file3"])
        post.photo4 = save_image(files["file4"])
        post.photo5 = save_image(files["file5"])
        with dbm.DBManager.session() as session:
            session.add(post)
            session.commit()
            new_id = post.id
       
        return new_id
       
    @staticmethod
    def delete_post(post_id):
        post = PostManager.get_post(post_id)
        with dbm.DBManager.session() as session:
            session.delete(post)
            session.commit()
    
    @staticmethod
    def update_post(post_id, form_data, files):
        with dbm.DBManager.session() as session:
        
            post = session.query(pt.Post).filter(pt.Post.id==post_id).first()
            post.title = form_data["post_title"]
            post.brand =  form_data["post_brand"]
            post.model =  form_data["post_model"]
            post.price = form_data["post_price"]
            post.year_made =  form_data["post_year_made"]
            post.mileage_km =form_data["post_mileage_km"]
            post.car_body = form_data["post_car_body"]
            post.feul = form_data["post_feul"]
            post.cubic = form_data["post_cubic"]
            post.engine_power_hp = form_data["post_engine_power_hp"]
            post.photo1 = post.photo1 if files["file1"].filename == "" else save_image(files["file1"])
            post.photo2 =  post.photo2 if files["file2"].filename == "" else save_image(files["file2"])
            post.photo3 =  post.photo3 if files["file3"].filename == "" else save_image(files["file3"])
            post.photo4 =  post.photo4 if files["file4"].filename == "" else save_image(files["file4"])
            post.photo5 = post.photo5 if files["file5"].filename == "" else save_image(files["file5"])
            post.transmission = form_data["post_transmission"]
            post.original_color = form_data["post_original_color"]
            post.climate = form_data["post_climate"]
            post.doors = form_data["post_doors"]
            post.country_id = int(form_data["post_country"])
            
            session.commit()

        return PostManager.get_post(post_id)
    
        
    @staticmethod
    def get_post(post_id:int):
        with dbm.DBManager.session() as session:
            return session.query(pt.Post).filter(pt.Post.id==post_id).first()
                
    @staticmethod
    def get_post_as_dict(post_id:int):
        post = PostManager.get_post(post_id)
        return pt.Post.to_dict(post)
    
    @staticmethod
    def all_posts():
        with dbm.DBManager.session() as session:
            return session.query(pt.Post).order_by(desc(pt.Post.posted)).all()
        
    @staticmethod
    def all_posts_as_dict():
        posts = PostManager.all_posts()
        posts_list = []
        for post in posts:
            posts_list.append(pt.Post.to_dict(post))
        return posts_list
    
    @staticmethod
    def get_posts_by_user_id(user_id):
        with dbm.DBManager.session() as session:
            return session.query(pt.Post).filter(pt.Post.user_id==user_id).all()
        
        
    @staticmethod
    def search_for_brand(brand):
        with dbm.DBManager.session() as session:
            return session.query(pt.Post).filter(pt.Post.brand==brand).all()
        
    @staticmethod
    def search_for_car_body(car_body):
        with dbm.DBManager.session() as session:
            return session.query(pt.Post).filter(pt.Post.car_body==car_body).all()
        
    @staticmethod
    def search_for_feul(feul):
        with dbm.DBManager.session() as session:
            return session.query(pt.Post).filter(pt.Post.feul==feul).all()
    
          
    @staticmethod
    def search_by_brand_car_body_fuel(brand, car_body, fuel):
        with dbm.DBManager.session() as session:
            filter_keys = []
            if fuel:
                filter_keys.append(pt.Post.feul == fuel)
            if car_body:
                filter_keys.append(pt.Post.car_body == car_body)
            if brand:
                filter_keys.append(pt.Post.brand == brand)
            return session.query(pt.Post).filter(*filter_keys).all()