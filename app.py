import pickle
from flask import Flask, render_template, request, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import sklearn, numpy
import os
import re
from flask_migrate import Migrate


app = Flask(__name__)
#Add Database
app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql://kwsywgxyvxsepf:ce54802d0d68f7ab422f1811f1fdb43bb5afd636b4fd44321a6bd827f1a146e6@ec2-3-223-242-224.compute-1.amazonaws.com:5432/d2v8qu0kf0g8f4'

#Initialize Database
db = SQLAlchemy(app)
migrate=Migrate(app, db)

class Inbox(db.Model):
    __tablename__='inbox'
    id = db.Column(db.Integer, primary_key = True)
    level = db.Column(db.String(10))
    num = db.Column(db.String(20))
    message = db.Column(db.String(150))
    lat = db.Column(db.Float(50))  
    lon = db.Column(db.Float(50))

    def __repr__(self):
        return '<Inbox %r>' % (self.level)

@app.route('/')
def home():
    return render_template('home.html')  
    

@app.route('/process', methods=['POST'])
def process():
    content_type = request.headers.get('Content-Type')
    if content_type !='application/json' :
        return {'status' : 'incompatible'}

    #JSON to form
    message = request.json['message']
    num = request.json['num']
    lat = request.json['lat']
    lon = request.json['lon']
    
    # Load Model and DataTransform
    model, loaded_tfidfvec = load_model()

    # Transform Data
    transformed_message = loaded_tfidfvec.transform([message])

    # Predict query
    prediction = model.predict(transformed_message)[0]
    inbox = Inbox(level= prediction, num = num, message = message, lat = lat, lon = lon )
    db.session.add(inbox)
    db.session.commit()
    return jsonify({'level': prediction , 'status' : 'success'})

    
# Function
def load_model():
    model_file_name = 'model/stack_model_p.pkl'
    data_transform_file_name = 'model/tfidf_params.pkl'
    
    with open(model_file_name, 'rb') as infile:
        model = pickle.load(infile)

    with open(data_transform_file_name, 'rb') as infile:
        loaded_tfidfvec = pickle.load(infile)
        
    return model, loaded_tfidfvec, 

@app.route('/inbox', methods=['GET'])
def inbox():
    return render_template('inbox.html')

if __name__=='__main__':
    app.run()