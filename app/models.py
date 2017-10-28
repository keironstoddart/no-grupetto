from app import db

class Athlete(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(64), index=True, unique=True)
    token = db.Column(db.String(64), index=True, unique=True)

    def __repr__(self):
        return '<User %r>' % (self.name)
