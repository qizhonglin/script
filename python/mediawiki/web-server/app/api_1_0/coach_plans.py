from flask import jsonify, request

from . import api
from ..models import CoachPlanPackage, CoachPlan

from ..exceptions import ValidationError

@api.route('/coachplanpackages')
def get_coachplanpackage():
    """
    /coachplanpackages?id=id_value&name=name_value
    """
    id = request.args.get('id', None)
    name = request.args.get('name', None)
    if id:
        coach_plan_package = CoachPlanPackage.query.filter_by(packageid=id).first_or_404()
        return jsonify(coach_plan_package.to_json())
    elif name:
        coach_plan_package = CoachPlanPackage.query.filter_by(name=name).first_or_404()
        return jsonify(coach_plan_package.to_json())
    else:
        raise ValidationError('the API format is wrong')


@api.route('/coachplans/<packagename>/cards')
def get_coachplan(packagename):
    coach_plan_package = CoachPlanPackage.query.filter_by(name=packagename).first_or_404()
    coach_plans = CoachPlan.query.filter_by(coach_plan_package=coach_plan_package).all()
    cards = [coach_plan.card.to_json() for coach_plan in coach_plans]
    return jsonify(cards)