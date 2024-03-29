from flask import Flask
from config import Config

from flask_migrate import Migrate
from flask_moment import Moment
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_turnstile import Turnstile
from flask_wtf.csrf import CSRFProtect

# declare extension instances outside so blueprints can still do `from app import db` etc.
csrf = CSRFProtect()
db = SQLAlchemy()
migrate = Migrate()
moment = Moment()
login_manager = LoginManager()
login_manager.login_view = "admin.login"
turnstile = Turnstile()

def create_app(config_class=Config):
    # create app variable (Flask instance)
    app = Flask(__name__)
    app.config.from_object(config_class)

    # init extensions
    csrf.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    moment.init_app(app)
    login_manager.init_app(app)
    turnstile.init_app(app)

    # register blueprints
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix="/admin")

    from app.blog import bp as blog_bp
    from app.blog.blogpage import bp as blog_blogpage_bp
    # "name" param must match blog_id in "Post" db table
    # This makes the endpoints "blog.0.index", "blog.1.index" etc.
    blog_bp.register_blueprint(blog_blogpage_bp, url_prefix="/professor-google",
            name="0")
    blog_bp.register_blueprint(blog_blogpage_bp, url_prefix="/writers-block",
            name="1")
    blog_bp.register_blueprint(blog_blogpage_bp, url_prefix="/writers-unblock",
            name="2")
    app.register_blueprint(blog_bp, subdomain="blog")

    return app

from app import models # imports done at bottom to prevent circular imports
