from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)

#Add Database
app.config['SQLALCHEMY_DATABASE_URI'] ='postgres://ruvxlwwhcmievw:e0234ccf6a73ae505d15d4e6a816f1d0a386ed66b2eedee1d27cb395243e8739@ec2-54-161-255-125.compute-1.amazonaws.com:5432/ddk9t1ob7o082d'
app.config['SECRET_KEY'] = 'smsclassification'

#Initialize Database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

#Create Model
class Inbox(db.Model):
    __tablename__ = 'Inbox'
    id = db.Column('student_id', db.Integer, primary_key = True)
    level = db.Column(db.String(10))
    num = db.Column(db.String(20))
    message = db.Column(db.String(150))
    lat = db.Column(db.Float(50))  
    lon = db.Column(db.Float(50))

    def __init__(self, level, num, message, lat, lon):
        self.level = level
        self.num = num
        self.message = message
        self.lat = lat
        self.lon = lon

if __name__ == '__main__':
    manager.run()