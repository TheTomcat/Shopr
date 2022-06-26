from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=app.config['SQLITE_BATCH_MODE'])

    from app.api import bp as api_bp
    app.register_blueprint(api_bp)

    return app

from app import models