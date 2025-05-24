import requests, json
from flask import Flask, render_template, jsonify, request, session, redirect, url_for, send_file
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = 'Sapientia'
CORS(app)

def query_graphdb(endpoint_url, sparql_query):
    # Set up the headers
    headers = {
        'Accept': 'application/json',  # You can change this based on the response format you need
    }
    
    # Make the GET request to the GraphDB endpoint
    response = requests.get(endpoint_url, params={'query': sparql_query}, headers=headers)
    
    if response.status_code == 200:
        return response.json()  # Return the JSON response from the GraphDB endpoint
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")
    
endpoint = "http://localhost:7200/repositories/sapientia"

query_24 = """
INSERT {
	?a :estudaCom ?m .
} WHERE {
    {?a a :Aprendiz ;
       :aprende ?d .
    ?m a :Mestre ;
       :ensina ?d .}
}
"""

query_25 = """
INSERT {
	?d :dáBasesPara ?a .
} WHERE {
    {?a a :Aprendiz ;
       :aprende ?d .
    ?m a :Mestre ;
       :ensina ?d .}
}
"""