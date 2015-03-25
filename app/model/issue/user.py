from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(80))
    number = db.Column(db.String(16), unique=True)
    password = db.Column(db.String(64))
    is_admin = db.Column(db.Boolean)
    teams = db.relationship('Team', backref=db.backref('user'))


    def __init__(self, name, number, password):
        self.name = name
        self.number = number
        self.password = password

    def __repr__(self):
        return '<User %r %r>' % (self.name, self.number)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'number': self.number,
            'password': self.password,
            'is_admin': self.is_admin

        }

