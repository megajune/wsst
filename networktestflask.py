#!/usr/bin/env python
# encoding: utf-8
import json
from socket import gethostbyname
import requests
from datetime import datetime
from flask import Flask, request, jsonify, make_response

app = Flask(__name__)
@app.route('/')

def contest():
    try:
        #Attempt DNS resolution against desthost. Return a error if unable to do so.
        t1 = gethostbyname(request.args['desthost'])
        #Attempt to access the target web server.
        t2 = requests.get(request.args['proto']+"://"+request.args['desthost']+":"+request.args['destport'])
    except Exception:
        error = []
        if t2.status_code not in [200,301,302]:
            error.append("This application was unable to connect to " + t2 + " with a HTTP connection.")
        if t1 == "":
            error.append(" DNS could not resolve" + request.args['desthost'])
        #error = "DNS could not resolve " + request.args['desthost'] + ", there is a problem in your local network, or the web server is down."   
    #If the error variable is set, it will be in the "locals" variable
    #if 'error' not in locals():
    if error.count == 0:
        #If the locals() method confirms the error variable was never defined, do the following:
        response = make_response(
                jsonify(
                    {"servername": request.args['desthost'], "message": request.args['desthost'] + " resolved to " + t1 + " and returned a HTTP status code of " + str(t2.status_code) }
                ),
                200,
            )
    else:
        #If error was defined, return a negative error status with a http 418
        response = make_response(
                jsonify(
                    {"servername": request.args['desthost'], "message": request.args['desthost'] + error}
                ),
                #Return an HTTP 418 if an error was detected
                418,
            )
    response.headers["Content-Type"] = "application/json"
    return response

if __name__ == "__main__":
     # Launch the Flask dev server
    app.run(host="0.0.0.0", ssl_context='adhoc')