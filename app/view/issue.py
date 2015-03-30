# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, redirect, url_for, g,jsonify
from app import db, app
from app.model.issue.issue import Issue, TrackRecord, Team
import datetime, time
from app.util import login_required, require_issue_auth

mod = Blueprint('issue', __name__, url_prefix='/issue')


@mod.route('/')
@login_required
def index():
    tag =  request.args.get('tag', None)
    team_name = u'全部'
    issues = []
    if tag:
        issues = Issue.query.filter(Issue.desc.like('%' + tag + '%')).all()
        team_name = u'与"' + tag + u'"相关'
    else:
        tid = request.args.get('tid', None)

        if not tid:
            issues = Issue.query.order_by(Issue.status.desc()).order_by(Issue.id.desc()).all()
        else:
            team = Team.query.filter_by(id=tid).first()
            if team:
                issues = team.issues
                team_name = team.name
            else:
                issues = Issue.query.order_by(Issue.status.desc()).order_by(Issue.id.desc()).all()

    return render_template('issue/index.html', issues=issues, team_name=team_name, user=g.user)


@mod.route('/add', methods=['GET','POST'])
@login_required
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
@require_issue_auth
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
@require_issue_auth
def delete(sid):
    x = Issue.query.filter_by(id=sid).first()
    db.session.delete(x)
    db.session.commit()
    return redirect(url_for("issue.index"))


@mod.route('/<sid>/close')
@require_issue_auth
def close(sid):
    x = Issue.query.filter_by(id=sid).first()
    x.status = "Close"


    close_time = datetime.date.today().strftime('%Y/%m/%d')
    close_content = u"问题关闭"

    t = TrackRecord(close_time, close_content, x.id)
    db.session.add(t)
    db.session.commit()

    return redirect(url_for("issue.index"))


@mod.route('/<sid>/open')
@require_issue_auth
def open(sid):
    x = Issue.query.filter_by(id=sid).first()
    x.status = "Open"

    t = TrackRecord(datetime.date.today().strftime('%Y/%m/%d'), u"问题打开", x.id)
    db.session.add(t)
    db.session.commit()
    return redirect(url_for("issue.edit", sid=sid))


@mod.route('/<sid>/track/add', methods=['POST'])
@require_issue_auth
def add_track(sid):
    time = request.form.get('time', "")
    content = request.form.get('content', "")

    t = TrackRecord(time, content, sid)
    db.session.add(t)
    db.session.commit()
    return str(t.id)


@mod.route('/<sid>/track/del', methods=['POST'])
@require_issue_auth
def del_track(sid):
    Issue

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
@login_required
def export():
    import xlwt

    style_header = xlwt.easyxf('pattern: pattern solid, fore_colour dark_teal; font: bold on,colour_index white;borders:top 1,bottom 1, left 1, right 1, top_colour gray40 , bottom_colour gray40, left_colour gray40, right_colour gray40')
    style_issue_open = xlwt.easyxf(
        'pattern: pattern solid, fore_colour white ; font: colour_index gray80 ;borders:top 1,bottom 1, left 1, right 1, top_colour gray40 , bottom_colour gray40, left_colour gray40, right_colour gray40;align: wrap on')
    style_issue_close = xlwt.easyxf(
        'pattern: pattern solid, fore_colour white ; font: colour_index gray40 ;borders:top 1,bottom 1, left 1, right 1, top_colour gray40 , bottom_colour gray40, left_colour gray40, right_colour gray40;align: wrap on')



    wb = xlwt.Workbook()
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
    issues = []
    if g.user.is_admin:
        issues = Issue.query.order_by(Issue.status.desc()).order_by(Issue.id.desc()).all()
    else:
        for team in g.user.teams:
            issues.extend(Issue.query.filter_by(team_id=team.id).order_by(Issue.status.desc()).order_by(Issue.id.desc()).all())
    for index, issue in enumerate(issues):
        style = style_issue_open
        if issue.status == "Close":
            style = style_issue_close
        ws.write(index + 1, 0, issue.site, style)
        ws.write(index + 1, 1, issue.desc, style)
        ws.write(index + 1, 2, issue.product, style)
        ws.write(index + 1, 3, issue.version, style)
        ws.write(index + 1, 4, issue.liaison, style)
        ws.write(index + 1, 5, issue.create_time, style)

        team = Team.query.filter_by(id=issue.team_id).first()
        ws.write(index + 1, 6, team.name, style)
        ws.write(index + 1, 7, issue.responsible, style)
        ws.write(index + 1, 8, issue.status, style)

        tracks = ''

        for i, t in enumerate(issue.tracks):
            if i != 0:
                tracks += "\n"
            tracks += t.time + ' ' + t.content
        ws.write(index + 1, 9, tracks, style)


    filename = str(time.time()) + ".xls"

    path = app.config.get('EXPORT_PATH') + filename

    wb.save(path)
    return redirect(url_for('static', filename='export/' +filename))

