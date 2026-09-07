import os
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()

def init_db(app):

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
    
    db.init_app(app)
    migrate.init_app(app, db)

    return