from datetime import datetime
from flask import render_template, session, redirect, url_for, request

from . import main
from .forms import NameForm
from .. import db
from ..models import User

@main.route('/login', methods=['GET', 'POST'])
def login():
	form = NameForm()
	if request.method == 'POST':
		if form.validate_on_submit():
			name = form.name.data
			form.name.data = ''
			return render_template('user.html', name=name, current_time=datetime.utcnow())
	else:
		return render_template('login.html', form=NameForm())
