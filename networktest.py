import socket
import argparse
import requests
import json 

parser = argparse.ArgumentParser(description='Test for network availability.')
parser.add_argument('--desthost', default='google.com', type=str, help='An connection will be attempted against this hostname')
parser.add_argument('--destport', default='443',help='A connection will be attempted using this port number')
parser.add_argument('--proto', default='https',help='This will typically be https')
args = parser.parse_args()

def basicnetworktest():
    try:
        #Attempt DNS resolution against desthost. Return a error if unable to do so.
        t1 = socket.gethostbyname(args.desthost)
    except Exception:
        error = "--DNS could not resolve " + args.desthost
        return error
    try:
        #Try to make a web connection. Return a error if unable to do so.
        t2 = requests.get(args.proto+"://"+args.desthost+":"+args.destport)
    except Exception:
        error = "--Could not make an HTTP connection to  " + args.desthost 
        return error
    if 'error' not in locals():
        #If error was never defined, return a positive status 
        return args.desthost + " resolved to " + t1 + " and returned a HTTP status code of " + str(t2.status_code)

#Return the results in the form of JSON
basictest2json =  '{ "destination":"'+args.desthost+'", "status":"'+str(basicnetworktest())+'"}'
status = json.loads(basictest2json)
print(status)