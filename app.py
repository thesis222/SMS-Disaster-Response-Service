from flask import Flask, jsonify, request, render_template, url_for, session, redirect
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
import pickle
import folium
from datetime import datetime
import pytz
from pandas import DataFrame
import string


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
    sender = request.json['sender']
    latitude = request.json['latitude']
    longitude = request.json['longitude']

    print(message, sender, latitude, longitude)

    # DateTime
    PHT = pytz.timezone('Asia/Manila')
    datetime_now = datetime.now(PHT)
    dateandtime = datetime_now.strftime("%d-%m-%Y %H:%M:%S")
    
    # Load Model and DataTransform
    model, loaded_tfidfvec = load_model()

    #Preprocess
    
    clean_msg = message.translate(str.maketrans('', '', string.punctuation))

    msg_lower = clean_msg.lower()
    msg_help = msg_lower.replace("tulong", "")

    # Transform Data
    transformed_message = loaded_tfidfvec.transform([msg_help])

    # Predict query
    prediction = model.predict(transformed_message)[0]

    if message and sender and latitude and longitude and request.method == 'POST':
        id = mongo.db.test.insert_one({
                'level':prediction,
                'message':message,
                'sender':sender,
                'latitude':latitude,
                'longitude':longitude,
                'datetime':dateandtime})

        return jsonify({'level' : prediction, 'status' : 'success'})

        

# Function
def load_model():
    model_file_name = 'model/stack_model_p.pkl'
    data_transform_file_name = 'model/tfidf_final.pkl'
    
    with open(model_file_name, 'rb') as infile:
        model = pickle.load(infile)

    with open(data_transform_file_name, 'rb') as infile:
        loaded_tfidfvec = pickle.load(infile)
        
    return model, loaded_tfidfvec 

#   INBOX PAGE-------------
#Table for Inbox
@app.route('/inbox', methods = ['GET', 'POST'])
def table():

    if request.method == 'GET':
        inbox = (mongo.db.test.find())

    return render_template('inbox.html', inbox = inbox )
#Update for Inbox
@app.route('/update/<id>')
def update(id):
    mongo.db.test.find_one_and_update({"_id":ObjectId(id)}, {"$set": { "status" : "on going" }})
    return redirect('/inbox')
#Delete for Inbox
@app.route('/delete1/<id>')
def delete1(id):
    mongo.db.test.find_one_and_update({"_id":ObjectId(id)}, {"$set": { "status" : "delete" }})
    return redirect('/inbox')

#   ON GOING PAGE-----------
#Table for On Going
@app.route('/ongoing', methods = ['GET'])
def ongoing():

    if request.method == 'GET':
        inbox = (mongo.db.test.find({"status": "on going"}))

    return render_template('on_going.html', inbox = inbox )
#Update for On Going
@app.route('/update1/<id>')
def update1(id):
    mongo.db.test.find_one_and_update({"_id":ObjectId(id)}, {"$set": { "status" : "responded" }})
    return redirect('/ongoing')
#Delete for On Going
@app.route('/delete2/<id>')
def delete2(id):
    mongo.db.test.find_one_and_update({"_id":ObjectId(id)}, {"$set": { "status" : "delete" }})
    return redirect('/ongoing')

#   RESPONDED PAGE----------
#Table for Responded
@app.route('/responded', methods = ['GET'])
def responded():

    if request.method == 'GET':
        inbox = (mongo.db.test.find({"status": "responded"}))

    return render_template('responded.html', inbox = inbox )

#Delete for Responeded
@app.route('/delete3/<id>')
def delete3(id):
    mongo.db.test.find_one_and_update({"_id":ObjectId(id)}, {"$set": { "status" : "delete" }})
    return redirect('/responded')

#   ARCHIVED PAGE
#Table for Archive
@app.route('/archived', methods = ['GET'])
def archived():

    if request.method == 'GET':
        inbox = (mongo.db.test.find({"status": "delete"}))

    return render_template('archived.html', inbox = inbox )
#Recover
@app.route('/recover/<id>')
def recover(id):
    mongo.db.test.find_one_and_update({"_id":ObjectId(id)}, {"$set": { "status" : "message" }})
    return redirect('/archived')
#Permanent Delete
@app.route('/delete/<id>')
def delete(id):
    mongo.db.test.delete_one({"_id":ObjectId(id)})
    return redirect('/archived')

#   MAP-----------
@app.route('/map')
def base():

    # this is base map
    map = folium.Map(
        location=[13.7565, 121.0583],
        zoom_start=11
    )

    #Dataframe
    low = DataFrame(list(mongo.db.test.find({"level" : "Low"})))
    moderate = DataFrame(list(mongo.db.test.find({"level" : "Moderate"})))
    high = DataFrame(list(mongo.db.test.find({"level" : "High"})))

    #Marker
    #Low
    for i in range (0, len(low)):

            html=f"""
            <h1>Low</h1>
            <p><b>Sender:</b> {low.iloc[i]['sender']}</p>
            <p><b>Message:</b> {low.iloc[i]['message']}</p>
            <p><b>Date & Time:</b> {low.iloc[i]['datetime']}</p>
            """
            iframe = folium.IFrame(html=html, width=300, height=170)
            popup = folium.Popup(iframe, max_width = 1000)

            folium.Marker(
                location = [low.iloc[i]['latitude'], low.iloc[i]['longitude']],
                popup = popup,
                icon = folium.Icon(color = 'green')
            ).add_to(map)

    #Moderate
    for i in range (0, len(moderate)):

            html=f"""
            <h1>Moderate</h1>
            <p><b>Sender:</b> {moderate.iloc[i]['sender']}</p>
            <p><b>Message:</b> {moderate.iloc[i]['message']}</p>
            <p><b>Date & Time:</b> {moderate.iloc[i]['datetime']}</p>
            """
            iframe = folium.IFrame(html=html, width=300, height=170)
            popup = folium.Popup(iframe, max_width = 1000)

            folium.Marker(
                location = [moderate.iloc[i]['latitude'], moderate.iloc[i]['longitude']],
                popup = popup,
                icon = folium.Icon(color = 'orange')
            ).add_to(map)

    #High
    for i in range (0, len(high)):

            html=f"""
            <h1>High</h1>
            <p><b>Sender:</b> {high.iloc[i]['sender']}</p>
            <p><b>Message:</b> {high.iloc[i]['message']}</p>
            <p><b>Date & Time:</b> {high.iloc[i]['datetime']}</p>
            """
            iframe = folium.IFrame(html=html, width=300, height=170)
            popup = folium.Popup(iframe, max_width = 1000)

            folium.Marker(
                location = [high.iloc[i]['latitude'], high.iloc[i]['longitude']],
                popup = popup,
                icon = folium.Icon(color = 'red')
            ).add_to(map)

    

    return map._repr_html_()

if __name__=='__main__':
    app.run(debug=True, port=5000)