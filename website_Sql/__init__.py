from flask import Flask 
from flask_mysqldb import MySQL
import MySQLdb.cursors
from flask_login import LoginManager, login_manager
from os import path

mysql = MySQL()

def create_app():
     app = Flask(__name__)

     app.config['SECRET_KEY'] = 'jsbdjsbds d fjsdbfs dnfjsdnf'
     app.config['MYSQL_HOST'] = 'localhost'
     app.config['MYSQL_USER'] = 'root'
     app.config['MYSQL_PASSWORD'] = 'Rmsprd@123'
     app.config['MYSQL_DB'] = 'geekprofile'
     mysql.init_app(app)
     from .views import views
     from .auths import auths


     login_manager = LoginManager()
     login_manager.login_view  = 'auths.login'
     login_manager.init_app(app)

     @login_manager.user_loader
     def load_user(id):
          cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
          cursor.execute('SELECT * FROM user WHERE id = %s', (id))
          user = cursor.fetchone()
          return user

     app.register_blueprint(views, url_prefix = "/");
     app.register_blueprint(auths, url_prefix = "/");
           
     return app

