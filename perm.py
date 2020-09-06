import urllib
import json
import os
import pgeocode
from flask import Flask
from flask import request
from flask import make_response
import json
import requests

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))
    print(type(req))
    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):

    result = req["queryResult"]
    parameters = result["parameters"]
    
   
    d1={
        "Bank Of Scotland":"atms/scotland.json",
        "Barclays Bank":"atms/barclays.json",
        "HSBC Group":"atms/hsbc.json",
        "Lloyds Bank":"atms/lloyds.json",
        "Santander UK PLC":"atms/santander.json"
    }

        
    if "age" in parameters.keys():
        n=parameters['age']
        #speech="you are "+str(int(n))+" years old"
        print("Response:")
        print(speech)
        return {
            "speech": speech,
            "displayText": speech,
            #"data": {},
            #"contextOut": [],
            "source": "BankRates",
            "fulfillmentText":speech
        }
    

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print ("Starting app on port %d" %(port))

    app.run(debug=True, port=port, host='0.0.0.0')