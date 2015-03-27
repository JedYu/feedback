from app import db


class Issue(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    site = db.Column(db.String(80))
    desc = db.Column(db.String(256))
    product = db.Column(db.String(64))
    version = db.Column(db.String(64))
    liaison = db.Column(db.String(64))
    create_time = db.Column(db.String(64))
    responsible = db.Column(db.String(64))
    status = db.Column(db.String(8))
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    tracks = db.relationship('TrackRecord', backref='issue',  order_by="desc(TrackRecord.time), desc(TrackRecord.id)")


    def __init__(self, site, desc, product, version, liaison, create_time, responsible, status):
        self.site = site
        self.desc = desc
        self.product = product
        self.version = version
        self.liaison = liaison
        self.create_time = create_time
        self.responsible = responsible
        self.status = status

    def __repr__(self):
        return '<Issue %r %r>' % (self.site, self.desc)


class TrackRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    time = db.Column(db.String(80))
    content = db.Column(db.String(256))
    issue_id = db.Column(db.Integer, db.ForeignKey('issue.id'))


    def __init__(self, time, content, issue_id):
        self.time = time
        self.content = content
        self.issue_id = issue_id

    def __repr__(self):
        return '<TrackRecord %r %r>' % (self.time, self.content)



class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(80), unique=True)
    manager_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    issues = db.relationship('Issue', backref=db.backref('team'), lazy='dynamic', order_by="desc(Issue.id), desc(Issue.status)")


    def __init__(self, name, manager_id):
        self.name = name
        self.manager_id = manager_id

    def __repr__(self):
        return '<Team %r>' % (self.name)
