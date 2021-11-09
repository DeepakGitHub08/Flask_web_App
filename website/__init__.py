from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_manager
from os import path

db = SQLAlchemy()
DB_NAME = "database.db"
def create_app():
     app = Flask(__name__)
     app.config['SECRET_KEY'] = 'jsbdjsbds d fjsdbfs dnfjsdnf'
     app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
     db.init_app(app) 

     from .views import views
     from .auths import auths
     from .model import User, Notes

     create_Database(app)

     login_manager = LoginManager()
     login_manager.login_view  = 'auths.login'
     login_manager.init_app(app)

     @login_manager.user_loader
     def load_user(id):
          return User.query.get(int(id))

     app.register_blueprint(views, url_prefix = "/");
     app.register_blueprint(auths, url_prefix = "/");
           
     return app

def create_Database(app):
     if not path.exists('website/' + DB_NAME):
          db.create_all(app= app)
