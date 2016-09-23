
from flask import render_template, session, redirect, url_for, request

from . import main

from ..services.KnowledgeParser import KnowledgeParser


@main.route('/medication/<id>')
def get_medication(id):
    knowledge_parser = KnowledgeParser()
    medication = knowledge_parser.parse_byid(id)

    # from pprint import pprint
    # pprint(medication)

    return render_template('medication.html', medication=medication)

@main.route('/medicationbyname/<name>')
def get_medication_byname(name):
    knowledge_parser = KnowledgeParser()
    medication = knowledge_parser.parse_bytitles(name)
    return render_template('medication.html', medication=medication)
