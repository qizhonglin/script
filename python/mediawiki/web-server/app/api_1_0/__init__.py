from flask import Blueprint

api = Blueprint('api', __name__)

from . import medications, coach_plans, errors
