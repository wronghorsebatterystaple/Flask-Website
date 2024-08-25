from flask import Flask, jsonify, redirect, url_for
from flask_cors import CORS
from flask_migrate import Migrate
from flask_moment import Moment
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_talisman import Talisman
from flask_turnstile import Turnstile
from flask_wtf.csrf import CSRFProtect, CSRFError

from config import Config


# declare extension instances outside so blueprints can still do `from app import db` etc.
cors = CORS(origins=Config.ALLOWED_ORIGINS, supports_credentials=True)
csrf = CSRFProtect()
db = SQLAlchemy(session_options={"autoflush": True}) # autoflush allows our post editing code to work properly
login_manager = LoginManager()
login_manager.login_view = Config.LOGIN_VIEW
migrate = Migrate()
moment = Moment()
talisman = Talisman()
turnstile = Turnstile()
# not using session_protection="strong" to avoid potential security mess of finding original IP through Cloudflare
# and Nginx; and more crucially IPv4 vs. IPv6 hell


import app.routes as global_routes # after initializing global extension variables to prevent circular imports


def create_app():
    # create app variable and config
    app = Flask(__name__)
    app.config.from_object(Config)

    app.jinja_env.lstrip_blocks = Config.JINJA_LSTRIP_BLOCKS
    app.jinja_env.trim_blocks = Config.JINJA_TRIM_BLOCKS

    # register blueprints
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix="/admin")

    from app.blog import bp as blog_bp
    from app.blog.blogpage import bp as blog_blogpage_bp
    # "name" param must match blogpage_id in "Post" db table
    # This makes the endpoints "blog.0.index", "blog.1.index" etc.
    for k, v in Config.BLOGPAGE_ID_TO_PATH.items():
        blog_bp.register_blueprint(blog_blogpage_bp, url_prefix=v, name=k)
    app.register_blueprint(blog_bp, subdomain="blog")

    # register global routes and stuff
    register_global_routes(app)

    # init extensions after all that
    cors.init_app(app)
    csrf.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    moment.init_app(app)
    login_manager.init_app(app)
    talisman.init_app(
            app,
            content_security_policy=Config.CSP,
            content_security_policy_nonce_in=["script-src", "script-src-attr", "script-src-elem"])
    turnstile.init_app(app)

    return app


from app import models # at the bottom to prevent circular imports


# Can't use `@app.route` in global routes.py (no global `app` variable), hence doing it this way
def register_global_routes(app):
    app.context_processor(global_routes.inject_login_form)
    app.context_processor(global_routes.inject_blogpages_from_db)
    app.add_url_rule("/bot-jail", view_func=global_routes.bot_jail, methods=["GET"])
    app.register_error_handler(CSRFError, global_routes.handle_csrf_error)
