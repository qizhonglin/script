from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from config import config

from flask_admin import Admin


bootstrap = Bootstrap()
db = SQLAlchemy()
admin = Admin(name='Knowledge Server Admin', template_mode='bootstrap3')


def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config[config_name])
	config[config_name].init_app(app)

	bootstrap.init_app(app)
	db.init_app(app)
	admin.init_app(app)

	from .main import main as main_blueprint
	app.register_blueprint(main_blueprint)

	from .api_1_0 import api as api_1_0_blueprint
	app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')


	return app

