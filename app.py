import pickle
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
#Add Database
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inbox.sqlite3'

#Initialize Database
db = SQLAlchemy(app)

#Create model
class Inbox(db.Model):
    __tablename__= 'inbox'
    id = db.Column('student_id', db.Integer, primary_key = True)
    level = db.Column(db.String(10))
    num = db.Column(db.String(20))
    msg = db.Column(db.String(150))
    lat = db.Column(db.Float(50))  
    lon = db.Column(db.Float(50))

    #Create String
    #def __init__(self, level, num, msg, lat, lon):
    #self.level = level
    #self.num = num
    #self.msg = msg
    #self.lat = lat
    #self.lon = lon

@app.route('/', methods=['GET'])
def home():
 	return 'Hello World' #HTML  

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

    # Load Model and DataTransform
    model, loaded_tfidfvec = load_model()

    # Transform Data
    transformed_message = loaded_tfidfvec.transform([query])

    # Predict query
    prediction = model.predict(transformed_message)[0]
    smsmsg = Inbox(level= prediction, num = number, message = message, lat = lat, lon = lon )
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

if __name__=='__main__':
    app.run()
    #db.create_all()