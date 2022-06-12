from re import template
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
import os

from sqlalchemy.sql.functions import user
import car_app.database.DBEngine as dbe
import car_app.database.DBManager as dbm
import car_app.database.models.User as us
import car_app.database.models.Post as pt
import car_app.logic.UserManager as um
import car_app.logic.CountryManager as cm
import car_app.logic.PostManager as pm
from passlib.hash import pbkdf2_sha256
from sqlalchemy import or_
from config import ADMIN



# Putanja direktorijuma gde se nalazi 'app.py' (C:/putanja/do/direktorijuma)
ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
# Putanja do direktorijuma 'static' kreirana sa path join
STATIC_PATH = os.path.join(ROOT_PATH, "car_app", "static")
# Putanja do direktorijuma 'templates' kreirana sa path join
TEMPLATES_PATH = os.path.join(ROOT_PATH, "car_app", "templates")

# Podešavanje 'settings.ini' DBEngine-a
dbe.DBEngine.set_settings_path("settings.ini")

# Pokretanje aplikacije sa izmenama lokacija direktorijuma "static" i "templates" (sada u car_app)
app = Flask(__name__, static_folder=STATIC_PATH,
            template_folder=TEMPLATES_PATH)
# Secret key potreban za sesije (proizvoljni hash string)
app.config['UPLOAD_FOLDER'] = os.path.join("car_app", "static", "cars_images")
app.secret_key = "ddf125898a7753b2437df121b774a87b"

hash = pbkdf2_sha256.encrypt("password", rounds=200000, salt_size=16)

# Globalne promenljive - context procesor
class AuthMixin(object):
    def is_accessible(self):
        if not "user" in session:
            return False
        return session["user"]["email"] == ADMIN

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            session["error"] = "Protected route. Only admin can access this page."
            return redirect(url_for("home"))

class AdminModelView(AuthMixin, ModelView):
    pass

class AdminIndex(AuthMixin, AdminIndexView):
    pass

admin = Admin(app, name="admin", template_mode = "bootstrap4", index_view=AdminIndex())
admin.add_view(ModelView(pt.Post, dbm.DBManager.session()))
admin.add_view(ModelView(us.User, dbm.DBManager.session()))


@app.context_processor
def global_variables():
    return {
        "current_year": 2022
    }


@app.route("/")
def home():
    if "success" in session:
        success = session["success"]
        session.pop("success", None) 
    else:
        success = None
    return render_template("home.jinja", success=success) 


@app.route("/login", methods=['GET', 'POST'])
def login():
    if "user" in session:
        return redirect(url_for('home'))

    if request.method == "GET":
        return render_template("login.jinja")
    else:
        username = request.form['username']
        user = um.UserManager.find_user_for_username(username)
        if user:
            if pbkdf2_sha256.verify(request.form['password'], user.password):
                session['user'] = us.User.to_dict(user)
                return redirect(url_for('home'))

        return render_template("login.jinja", error="Username and/or password is incorrect.")


@app.route("/logout")
def logout():
    if "user" in session:
        session.pop("user", None)
    return  redirect(url_for('home'))

# Registracija

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        return render_template("register.jinja")
    else:
        new_user = us.User()
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        user = um.UserManager.find_user_for_username(username)
        if user:
            return render_template("register.jinja", error="Username already exists.")
        correct_email = um.UserManager.find_user_for_email(email)
        if correct_email:
            return render_template("register.jinja", error="Email already exists.")
        
        if len(username) < 3:
            return render_template("register.jinja", error="Your username must be greater than 3 character.")
        elif len(password) < 5:
            return render_template("register.jinja", error="Your password must be greater than 5 character.")
        else:
            new_user = us.User(username=username, email=email, password=pbkdf2_sha256.hash(password))
            with dbm.DBManager.session() as session:
                session.add(new_user)
                session.commit()
            return render_template("home.jinja", success="You are registred.")


@app.route("/posts")
def all_posts():
    posts = pm.PostManager.all_posts_as_dict()
    return render_template("posts/post_list.jinja", posts=posts)

@app.route("/posts/view/<int:post_id>")
def post_details(post_id:int):
    post = pm.PostManager.get_post_as_dict(post_id)
    return render_template("posts/single_post.jinja", post=post)

# Novi post

@app.route("/posts/new", methods=["GET", "POST"])
def new_post():
   if request.method=="GET":
       countries = cm.CountryManager.all_countries_as_dict()
       return render_template("posts/new_post.jinja", countries=countries)
   else:
       new_id = pm.PostManager.save_post(request.form, request.files, session["user"]["id"])
       return redirect(url_for('post_details', post_id=new_id))

# Update

@app.route("/posts/update/<int:post_id>", methods=["GET", "POST"])
def update_post(post_id:int):
    countries = cm.CountryManager.all_countries_as_dict()
    if request.method == "GET":
        post = pm.PostManager.get_post_as_dict(post_id)
        return render_template("posts/update_post.jinja", post=post, countries=countries)
    else:
        updated_post = pm.PostManager.update_post(post_id, request.form, request.files)
        updated_post = pt.Post.to_dict(updated_post)
        return render_template("posts/update_post.jinja",
               post=updated_post, countries=countries,
               success="Post has been successfully updated.")
        
@app.route("/profile/<string:username>")
def profile_details(username:str):
    user = um.UserManager.find_user_for_username(username)
    user = us.User.to_dict(user)
    return render_template("profile.jinja", user=user)

# Brisanje

@app.route("/posts/delete/<int:post_id>")
def delete_post(post_id:int):
    pm.PostManager.delete_post(post_id)
    session["success"] = "Post successfully deleted."
    return redirect(url_for('home'))

# Pretraga

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "GET":
        return render_template("search.jinja")
    else:
        brand = request.form["brand"]
        car_body = request.form["car_body"]
        fuel = request.form["fuel"]
        posts = pm.PostManager.search_by_brand_car_body_fuel(brand, car_body, fuel)
        return render_template("posts/post_list.jinja", posts=posts)


@app.route("/my_posts")
def my_posts():
    user = session.get("user")
    if "user" in session:
        posts = pm.PostManager.get_posts_by_user_id(user["id"])
        return render_template("posts/post_list.jinja", posts=posts)
    else:
        return render_template("message.jinja")