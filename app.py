import pickle
from flask import Flask, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
import sklearn, numpy
import os
import re
from flask_migrate import Migrate


app = Flask(__name__)
#Add Database
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///inbox.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Initialize Database
db = SQLAlchemy(app)

from models import User


@app.route('/')
def home():
    return render_template('home.html')  
    

@app.route('/process', methods=['POST'])
def process():
    content_type = request.headers.get('Content-Type')
    if content_type !='application/json' :
        return 'incompatible'

    #JSON to form
    message = request.json['message']
    num = request.json['number']
    lat = request.json['latitude']
    lon = request.json['longitude']

    print(message, num, lat, lon)
    
    # Load Model and DataTransform
    model, loaded_tfidfvec = load_model()

    # Transform Data
    transformed_message = loaded_tfidfvec.transform([message])

    # Predict query
    prediction = model.predict(transformed_message)[0]
    smsmsg = Inbox(level= prediction, num = num, message = message, lat = lat, lon = lon )
    db.session.add(smsmsg)
    db.session.commit()
    return prediction

    

# Function
def load_model():
    model_file_name = 'model/stack_model_p.pkl'
    data_transform_file_name = 'model/tfidf_params.pkl'
    
    with open(model_file_name, 'rb') as infile:
        model = pickle.load(infile)

    with open(data_transform_file_name, 'rb') as infile:
        loaded_tfidfvec = pickle.load(infile)
        
    return model, loaded_tfidfvec

@app.route('/inbox', methods=['GET'])
def inbox():
    return render_template('inbox.html')

if __name__=='__main__':
    app.run()