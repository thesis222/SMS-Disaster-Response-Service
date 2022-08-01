from manage import db,app

#Create Model
class Inbox(db.Model):
    __tablename__ = 'Inbox'
    id = db.Column('student_id', db.Integer, primary_key = True)
    level = db.Column(db.String(10))
    num = db.Column(db.String(20))
    message = db.Column(db.String(150))
    lat = db.Column(db.Float(50))  
    lon = db.Column(db.Float(50))

    def __repr__(self):
        return '<User %r>' % (self.level)