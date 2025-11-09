from flask import Flask
from .config import Config
from .extensions import db, migrate, jwt, api
from .routes.web import web_bp
from .api.auth import ns as auth_ns
from .api.tasks import ns as tasks_ns

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    api.init_app(app)

    # Register namespaces (API /docs at /api/)
    api.add_namespace(auth_ns, path="/auth")
    api.add_namespace(tasks_ns, path="/tasks")

    # Register blueprints (server-rendered)
    app.register_blueprint(web_bp)

    return app
