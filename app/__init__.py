from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from config import DevelopmentConfig
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy 

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = '请登录后访问'
bootstrap = Bootstrap()


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login.init_app(app)
    bootstrap.init_app(app)
    migrate.init_app(app, db)

    from app.engineer import bp as engineer_bp
    app.register_blueprint(engineer_bp, url_prefix='/engineer')

    from app.sales import bp as sales_bp
    app.register_blueprint(sales_bp, url_prefix='/sales')

    from app.hr import bp as hr_bp
    app.register_blueprint(hr_bp, url_prefix='/hr')

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    return app
