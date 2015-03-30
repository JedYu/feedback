# -*- coding: utf-8 -*-
from datetime import timedelta
from flask import Flask, session, g, render_template
from flask_sqlalchemy import SQLAlchemy
import config
from util import *

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)


@app.errorhandler(401)
@app.errorhandler(404)
@app.errorhandler(502)
def http_error(error):
    return render_template('error.html', error=error)


@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(hours=24)

@app.before_request
def load_current_user():
    from model.issue.issue import Team
    from model.issue.user import User
    g.user = User.query.filter_by(number=session['number']).first() if 'number' in session else None
    g.users = User.query.all()
    g.teams = Team.query.all()


from app.view import issue, manage

app.register_blueprint(manage.mod)
app.register_blueprint(issue.mod)



@app.route('/')
@login_required
def index():
    return redirect(url_for("issue.index"))
