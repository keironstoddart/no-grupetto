from app import db

class Athlete(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(64), index=True)
    token = db.Column(db.String(64), index=True, unique=True)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def get_token(self):
        return str(self.token)

    def __repr__(self):
        return '<User %r>' % (self.name)

class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    athlete_id = db.Column(db.Integer)
    bpm = db.Column(db.Float)
    strava_id = db.Column(db.Integer, unique=True)
    distance = db.Column(db.Float)
    elevation = db.Column(db.Float)
    calories = db.Column(db.Integer)
    speed = db.Column(db.Float)
    city = db.Column(db.String(64))
    state = db.Column(db.String(64))
    date = db.Column(db.DateTime)
    act_type = db.Column(db.String(64))
    name = db.Column(db.String(64))

    def __repr__(self):
        return '<Activity %r>' % (self.strava_id)

# class Segments(db.Model):
    # todo
