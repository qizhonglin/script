
from flask import render_template, session, redirect, url_for, request, abort, jsonify

from . import main

from ..services.KnowledgeParser import KnowledgeParser

from ..models import Card

@main.route('/medications')
def get_mediation():
    """
    /medications?id=id_value&name=name_value
    """
    print "enter /medications"
    id = request.args.get('id', None)
    name = request.args.get('name', None)
    medication = None
    if id:
        print u"id = {0}".format(id)
        medication = KnowledgeParser().parse_byid(id)
    if name:
        print u"name = {0}".format(name)
        medication = KnowledgeParser().parse_bytitles(name)
    return __render_template('medication.html', medication=medication)


@main.route('/ks/medications')
def get_medication_byname_viamap():
    """
    /ks/medications?name=name_value
    """
    name = request.args.get('name', None)
    medication = None
    if name:
        card = Card.query.filter_by(name=name).first()
        if card:
            medication = KnowledgeParser().parse_bytitles(card.wiki_title)
    return __render_template('medication.html', medication=medication)


def __render_template(view, medication):
    # from pprint import pprint
    # pprint(medication)

    if medication:
        return render_template(view, medication=medication)
    else:
        abort(404)
