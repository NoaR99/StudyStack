import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
bootstrap = Bootstrap5()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
migrate = Migrate()

basedir = os.path.abspath(os.path.dirname(__file__))

def create_app(config_class=Config):
    app = Flask(__name__, static_folder=os.path.join(basedir, 'static'), static_url_path='/static')
    app.config.from_object(config_class)

    db.init_app(app)
    bootstrap.init_app(app)

    login_manager.init_app(app)
    migrate.init_app(app, db)

    from app.auth.routes import auth_bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.decks.routes import decks_bp as decks_bp
    app.register_blueprint(decks_bp, url_prefix='/decks')

    from app.main.routes import main_bp as main_bp
    app.register_blueprint(main_bp)

    with app.app_context():
        db.create_all()

    return app

from app import models


