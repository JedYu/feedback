# -*- coding: utf-8 -*-

from flask import Flask, session, g, render_template
from flask_sqlalchemy import SQLAlchemy
import config
from util import *

app = Flask(__name__)
app.config.from_object(config)
print app.config.get('SQLALCHEMY_DATABASE_URI')
db = SQLAlchemy(app)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


from model.issue.issue import *
from model.issue.user import User


def create_tables():
    from model.issue.issue import Issue, Team
    from model.issue.user import User

    db.create_all()


def create_():
    u = User("YuJian", "00486", get_encrypt_passwd("123456"))
    u.is_admin = True
    db.session.add(u)

    u2 = User("test", "00001", get_encrypt_passwd("test"))
    db.session.add(u2)

    db.session.commit()

    print u.id

    t = Team(u"移动开发组", u.id)
    t2 = Team(u"<script> alert(1) </script>", u.id)
    db.session.add(t)
    db.session.add(t2)
    db.session.commit()

    x = Issue(u"某代理商", u"NVR202-08EP，B2308P08，手机客户端看到NVR在线但是无法播放实况", u"宇视云眼DCT", "M00010120B3305", "lisongwei",
              "2015/1/19", u"虞雪辰", "Open")
    db.session.add(x)
    db.session.commit()
    t.issues.append(x)
    t2.issues.append(x)

    db.session.commit()


def print_():
    users = User.query.all()
    print users

    teams = Team.query.all()
    print teams

    print teams[0].issues


# def test_db():
# x = Issue(u"某代理商",u"NVR202-08EP，B2308P08，手机客户端看到NVR在线但是无法播放实况",u"宇视云眼DCT","M00010120B3305","lisongwei","2015/1/19",u"虞雪辰","Open")
#
#     db.session.add(x)
#     db.session.commit()
#
#     t = TrackRecord(u"2015/3/4",u"问题是iOS系统限制引起。但长时间不上线问题，实验室尝试复现", 2)
#     db.session.add(t)
#     db.session.commit()
#
#
#     s = Issue.query.all()
#     print s[0].tracks

@app.before_request
def load_current_user():
    g.user = User.query.filter_by(number=session['number']).first() if 'number' in session else None
    g.users = User.query.all()
    g.teams = Team.query.all()

#
# @app.teardown_request
# def remove_db_session(exception):
#     db_session.remove()



from app.view import issue, manage

app.register_blueprint(manage.mod)
app.register_blueprint(issue.mod)

