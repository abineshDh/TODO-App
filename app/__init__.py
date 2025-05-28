from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config

# init. sqlalchemy and login_manager 
db = SQLAlchemy()
login_manager = LoginManager()
# redirect to auth.login if not logged in 
login_manager.login_view = 'auth.login'

def create_app():
    # creates flask app instance
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # init. extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    
    # create database
    from .models import User
    with app.app_context():
        db.create_all()
        
    from .api import api_bp
    from .auth import auth_bp
    from .routes import main_bp 
    
    # registers blueprints with app
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    
    return app
        
    