Thesis Title:
"Using Text Classification on Disaster Help-Related Messages"

Web Applciation in Heroku

A Web-based application for mapping the prediction results made by the classifier such as (Spam, Low, Moderate, and High) and for generating a map using a GIS platform to locate the user's position. Flask REST API is utilized to load the classification model and identify and categorize the received messages.

app.py - python flask code
Procfile - web: gunicorn app:app 
requirements.txt - libraries included
runtime.txt - python version


Folders:
model - pkl file of the text classification 
static - images
templates - html codes of every pages
