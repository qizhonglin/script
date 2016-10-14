from flask import jsonify, request

from . import api

from ..services.KnowledgeParser import KnowledgeParser

from ..models import Card

from ..exceptions import ValidationError


@api.route('/medications')
def get_mediation():
    """
    /medications?id=id_value&name=name_value
    """
    print "enter /medications"
    id = request.args.get('id', None)
    name = request.args.get('name', None)
    if id:
        print u"id = {0}".format(id)
        return jsonify(KnowledgeParser().parse_byid(id))
    elif name:
        print u"name = {0}".format(name)
        return jsonify(KnowledgeParser().parse_bytitles(name))
    else:
        raise ValidationError('the API format is wrong')


@api.route('/ks/medications')
def get_medication_byname_viamap():
    """
    /ks/medications?name=name_value
    """
    name = request.args.get('name', None)
    card = Card.query.filter_by(name=name).first_or_404()
    return jsonify(card.to_json())
