# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, redirect, url_for, g
from app import db, app
from app.model.issue.issue import Issue, TrackRecord, Team
import datetime, time
from app.util import login_required

mod = Blueprint('issue', __name__, url_prefix='/issue')


@mod.route('/')
@login_required
def index():
    team_name = request.args.get('team', '')

    issues = []
    if not team_name:
        issues = Issue.query.order_by(Issue.status.desc()).order_by(Issue.id.desc()).all()
    else:
        team = Team.query.filter_by(name=team_name).first()
        if team:
            issues = team.issues
    teams = Team.query.all()
    return render_template('issue/index.html', issues=issues, teams=teams, team_name=team_name, user=g.user)


@mod.route('/add', methods=['GET','POST'])
def add():
    if request.method == "POST":
        x = Issue(request.form.get('site', ''), request.form.get('desc', ''), request.form.get('product', ''),
                  request.form.get('version', ''), request.form.get('liaison', ''), request.form.get('create_time', ''),
                  request.form.get('responsible', ''), request.form.get('status', 'Open'))

        team_name = request.form.get('team', '')
        if not team_name:
            pass
        else:
            team = Team.query.filter_by(name=team_name).first()
            x.team_id = team.id
        db.session.add(x)
        db.session.commit()

        t = TrackRecord(datetime.date.today().strftime('%Y/%m/%d'), u"问题创建", x.id)
        db.session.add(t)
        db.session.commit()

        return redirect(url_for("issue.index"))
    else:
        return render_template('issue/create.html')


@mod.route('/<sid>/edit', methods=['POST', 'GET'])
def edit(sid):
    x = Issue.query.filter_by(id=sid).first()

    if request.method == "POST":
        x.site = request.form.get('site', '')
        x.desc = request.form.get('desc', '')
        x.product = request.form.get('product', '')
        x.version = request.form.get('version', '')
        x.liaison = request.form.get('liaison', '')
        x.create_time = request.form.get('create_time', '')
        x.responsible = request.form.get('responsible', '')

        team = Team.query.filter_by(name=request.form.get('team', '')).first()
        x.team_id = team.id
        db.session.commit()

        return ""
    else:
        teams = Team.query.all()
        return render_template('issue/edit.html', issue=x, teams=teams)


@mod.route('/<sid>/del')
def delete(sid):
    x = Issue.query.filter_by(id=sid).first()
    db.session.delete(x)
    db.session.commit()
    return redirect(url_for("issue.index"))


@mod.route('/<sid>/close')
def close(sid):
    x = Issue.query.filter_by(id=sid).first()
    x.status = "Close"

    t = TrackRecord(datetime.date.today().strftime('%Y/%m/%d'), u"问题关闭", x.id)
    db.session.add(t)
    db.session.commit()
    return redirect(url_for("issue.index"))


@mod.route('/<sid>/open')
def open(sid):
    x = Issue.query.filter_by(id=sid).first()
    x.status = "Open"

    t = TrackRecord(datetime.date.today().strftime('%Y/%m/%d'), u"问题打开", x.id)
    db.session.add(t)
    db.session.commit()
    return redirect(url_for("issue.index"))


@mod.route('/<sid>/track/add', methods=['POST'])
def add_track(sid):
    time = request.form.get('time', "")
    content = request.form.get('content', "")

    t = TrackRecord(time, content, sid)
    db.session.add(t)
    db.session.commit()
    return str(t.id)


@mod.route('/<sid>/track/del', methods=['POST'])
def del_track(sid):
    tid = request.form.get('id', -1)
    if tid == -1:
        return ""

    t = TrackRecord.query.filter_by(id=tid).first()

    if int(t.issue_id) != int(sid):
        return ""

    db.session.delete(t)
    db.session.commit()
    return ""


@mod.route('/export')
def export():
    import xlwt

    style_header = xlwt.easyxf('pattern: pattern solid, fore_colour dark_teal; font: bold on,colour_index white;borders:top 1,bottom 1, left 1, right 1, top_colour gray40 , bottom_colour gray40, left_colour gray40, right_colour gray40')
    style_data = xlwt.easyxf(
        'pattern: pattern solid, fore_colour white ; font: colour_index gray80 ;borders:top 1,bottom 1, left 1, right 1, top_colour gray40 , bottom_colour gray40, left_colour gray40, right_colour gray40')

    wb = xlwt.Workbook();
    ws = wb.add_sheet(u'局点问题')
    ws.write(0, 0, u"局点", style_header)
    ws.write(0, 1, u"问题描述", style_header)
    ws.write(0, 2, u"产品", style_header)
    ws.write(0, 3, u"版本", style_header)
    ws.write(0, 4, u"接口人", style_header)
    ws.write(0, 5, u"提交时间", style_header)
    ws.write(0, 6, u"责任项目组", style_header)
    ws.write(0, 7, u"责任人", style_header)
    ws.write(0, 8, u"状态", style_header)
    ws.write(0, 9, u"跟踪记录", style_header)

    ws.col(0).width = 0x0d00 * 2
    ws.col(1).width = 0x0d00 * 5
    ws.col(2).width = 0x0d00 * 2
    ws.col(3).width = 0x0d00 * 2
    ws.col(4).width = 0x0d00
    ws.col(5).width = 0x0d00
    ws.col(6).width = 0x0d00
    ws.col(7).width = 0x0d00
    ws.col(8).width = 0x0d00
    ws.col(9).width = 0x0d00 * 5
    issues = Issue.query.order_by(Issue.create_time.desc()).all()
    for index, issue in enumerate(issues):
        ws.write(index + 1, 0, issue.site, style_data)
        ws.write(index + 1, 1, issue.desc, style_data)
        ws.write(index + 1, 2, issue.product, style_data)
        ws.write(index + 1, 3, issue.version, style_data)
        ws.write(index + 1, 4, issue.liaison, style_data)
        ws.write(index + 1, 5, issue.create_time, style_data)

        team = Team.query.filter_by(id=issue.team_id).first()
        ws.write(index + 1, 6, team.name, style_data)
        ws.write(index + 1, 7, issue.responsible, style_data)
        ws.write(index + 1, 8, issue.status, style_data)

        tracks = ''
        for t in issue.tracks:
            tracks += t.time + ' ' + t.content + '\n'
        ws.write(index + 1, 9, tracks, style_data)


    filename = str(time.time()) + ".xls"

    path = app.config.get('EXPORT_PATH') + filename

    wb.save(path)
    return redirect(url_for('static', filename='export/' +filename))
#
# @mod.route('/search/')
# def search():
# q = request.args.get('q') or ''
# page = request.args.get('page', type=int) or 1
# results = None
# if q:
#         results = perform_search(q, page=page)
#         if results is None:
#             abort(404)
#     return render_template('general/search.html', results=results, q=q)
#
#
# @mod.route('/logout/')
# def logout():
#     if 'openid' in session:
#         flash(u'Logged out')
#         del session['openid']
#     return redirect(request.referrer or url_for('general.index'))
#
#
# @mod.route('/login/', methods=['GET', 'POST'])
# @oid.loginhandler
# def login():
#     if g.user is not None:
#         return redirect(url_for('general.index'))
#     if 'cancel' in request.form:
#         flash(u'Cancelled. The OpenID was not changed.')
#         return redirect(oid.get_next_url())
#     openid = request.values.get('openid')
#     if not openid:
#         openid = COMMON_PROVIDERS.get(request.args.get('provider'))
#     if openid:
#         return oid.try_login(openid, ask_for=['fullname', 'nickname'])
#     error = oid.fetch_error()
#     if error:
#         flash(u'Error: ' + error)
#     return render_template('general/login.html', next=oid.get_next_url())
#
#
# @mod.route('/first-login/', methods=['GET', 'POST'])
# def first_login():
#     if g.user is not None or 'openid' not in session:
#         return redirect(url_for('.login'))
#     if request.method == 'POST':
#         if 'cancel' in request.form:
#             del session['openid']
#             flash(u'Login was aborted')
#             return redirect(url_for('general.login'))
#         db_session.add(User(request.form['name'], session['openid']))
#         db_session.commit()
#         flash(u'Successfully created profile and logged in')
#         return redirect(oid.get_next_url())
#     return render_template('general/first_login.html',
#                            next=oid.get_next_url(),
#                            openid=session['openid'])
#
#
# @mod.route('/profile/', methods=['GET', 'POST'])
# @requires_login
# def profile():
#     name = g.user.name
#     if request.method == 'POST':
#         name = request.form['name'].strip()
#         if not name:
#             flash(u'Error: a name is required')
#         else:
#             g.user.name = name
#             db_session.commit()
#             flash(u'User profile updated')
#             return redirect(url_for('.index'))
#     return render_template('general/profile.html', name=name)
#
#
# @mod.route('/profile/change-openid/', methods=['GET', 'POST'])
# @requires_login
# @oid.loginhandler
# def change_openid():
#     if request.method == 'POST':
#         if 'cancel' in request.form:
#             flash(u'Cancelled. The OpenID was not changed.')
#             return redirect(oid.get_next_url())
#     openid = request.values.get('openid')
#     if not openid:
#         openid = COMMON_PROVIDERS.get(request.args.get('provider'))
#     if openid:
#         return oid.try_login(openid)
#     error = oid.fetch_error()
#     if error:
#         flash(u'Error: ' + error)
#     return render_template('general/change_openid.html',
#                            next=oid.get_next_url())
#
#
# @oid.after_login
# def create_or_login(resp):
#     session['openid'] = resp.identity_url
#     user = g.user or User.query.filter_by(openid=resp.identity_url).first()
#     if user is None:
#         return redirect(url_for('.first_login', next=oid.get_next_url(),
#                                 name=resp.fullname or resp.nickname))
#     if user.openid != resp.identity_url:
#         user.openid = resp.identity_url
#         db_session.commit()
#         flash(u'OpenID identity changed')
#     else:
#         flash(u'Successfully signed in')
#     return redirect(oid.get_next_url())
