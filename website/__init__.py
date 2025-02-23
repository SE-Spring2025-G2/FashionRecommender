from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user

import os

db = SQLAlchemy()
DB_NAME = "database.db"
db_overlay = None


def create_app(test_conifg=None):
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "hjshjhdjah kjshkjdhjs"
    # app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    sql_username = os.environ.get('DB_USER')
    sql_password = os.environ.get('DB_PASSWORD')
    sql_host = os.environ.get('DB_HOST')
    sql_db = os.environ.get('DB_NAME')
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = f'mysql+pymysql://{sql_username}:{sql_password}@{sql_host}:3306/fashion'

    if test_conifg:
        app.config["SECRET_KEY"] = test_conifg["SECRET_KEY"]
        app.config["SQLALCHEMY_DATABASE_URI"] = test_conifg["SQLALCHEMY_DATABASE_URI"]

    db.init_app(app)
    from .views import views
    from .auth import auth
    from .favourites import favouritesbp

    from . import preferences
    from . import recommendations
    from . import shopping
    from . import logos

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(favouritesbp, url_prefix="/")
    app.register_blueprint(preferences.preferencesbp)
    app.register_blueprint(recommendations.recommendationsbp)
    app.register_blueprint(shopping.shoppingbp)
    app.register_blueprint(logos.logosbp)

    from .models import User

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    @app.context_processor
    def inject_user():
        return dict(user=current_user)

    return app
