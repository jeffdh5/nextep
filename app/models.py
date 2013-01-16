from app import db

ROLE_USER = 0
ROLE_ADMIN = 1


class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nickname = db.Column(db.String(64), unique = True)
    email = db.Column(db.String(120), unique = True)
    role = db.Column(db.SmallInteger, default = ROLE_USER)
        
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)
        
    def __repr__(self):
        return '<User %r>' % (self.nickname)

class Show(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique = True)    
    tv_link = db.Column(db.String(64), unique = True)
    tv_rage_link = db.Column(db.String(64), unique = True)
    day = db.Column(db.String(64), db.ForeignKey('day.name'))

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<Show %r>' % (self.name)
        
class Day(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique = True)
    shows = db.relationship('Show', backref='day_of_show', lazy='dynamic')
    
    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<Day %r>' % (self.name)