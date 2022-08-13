from flask import Flask, jsonify, request, render_template, url_for, session
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
import pickle


app = Flask(__name__)

#Database Name
app.config['MONGO_DBNAME'] = "Testdb"
#Database URI
app.config['MONGO_URI'] = "mongodb+srv://root:pass@cluster0.r3n21no.mongodb.net/Testdb?retryWrites=true&w=majority"

mongo = PyMongo(app)


@app.route('/')
def home():
    return render_template('home.html')  
    

@app.route('/process', methods=['POST'])
def process():
    
    #JSON to form
    message = request.json['message']
    sender = request.json ['sender']
    receiver = request.json['receiver']
    latitude = request.json['latitude']
    longitude = request.json['longitude']

    # Load Model and DataTransform
    model, loaded_tfidfvec = load_model()

    # Transform Data
    transformed_message = loaded_tfidfvec.transform([message])

    # Predict query
    prediction = model.predict(transformed_message)[0]

    if message and sender and receiver and latitude and longitude and request.method == 'POST':
        id = mongo.db.test.insert_one({
                'level':prediction,
                'message':message,
                'sender':sender,
                'receiver':receiver,
                'latitude':latitude,
                'longitude':longitude})

        return jsonify({'level': prediction , 'status' : 'success'})
    return jsonify({'status' : 'incompatible'})

# Function
def load_model():
    model_file_name = 'model/stack_model_p.pkl'
    data_transform_file_name = 'model/tfidf_params.pkl'
    
    with open(model_file_name, 'rb') as infile:
        model = pickle.load(infile)

    with open(data_transform_file_name, 'rb') as infile:
        loaded_tfidfvec = pickle.load(infile)
        
    return model, loaded_tfidfvec 

@app.route('/inbox', methods = ['GET'])
def table():

    if request.method == 'GET':
        inbox = (mongo.db.test.find())

    return render_template('inbox.html', inbox = inbox )

if __name__=='__main__':
    app.run()