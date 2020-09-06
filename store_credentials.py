from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import os
"""
app = Flask(__name__)
api = Api(app)

@app.route("/")
def hello():
    return jsonify({"about " : "hello world!"})


@app.route("/", methods = ['GET', 'POST'])
def index():
    if (request.method == 'POST'):
        some_json = request.get_json()
        return jsonify({'you sent' : some_json}), 201
    else:
        return jsonify({"about":"Hello world!"})

@app.route('/multi/<int:num>', methods = ['GET'])
def get_multiply10(num):
    return jsonify({'result' : num * 10})
"""
"""
class HelloWorld(Resource):
    def get(self):
        return{'about' : 'Hello world'}
    def post(self):
        some_json = request.get_json()
        return {'you sent' : some_json}, 201

class Multi(Resource):
    def get(self, num):
        return {'result' : num * 10}

api.add_resource(HelloWorld, '/')
api.add_resource(Multi, '/multi/<int:num>')


if __name__ == '__main__':
    app.run(debug =  True)
"""


from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from datetime import datetime, timedelta
import pickle
email = input("Insert you email address please")
scopes = ['https://www.googleapis.com/auth/calendar']
flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", scopes=scopes)
credentials = flow.run_console()
pickle.dump(credentials, open(email + '.pkl', 'wb'))
#credentials = pickle.load(open('token.pkl', 'rb'))
service = build("calendar", "v3", credentials = credentials)
result = service.calendarList().list().execute()
calendar_id = result['items'][3]['id']

event = {
  'summary': 'teste ameahe',
  'location': '800 Howard St., San Francisco, CA 94103',
  'description': 'A chance to s.',
  'start': {
    'dateTime': '2023-05-28T09:00:00-07:00',
    'timeZone': 'America/Los_Angeles',
  },
  'end': {
    'dateTime': '2023-05-28T17:00:00-07:00',
    'timeZone': 'America/Los_Angeles',
  },
  'reminders': {
    'useDefault': False,
    'overrides': [
      {'method': 'email', 'minutes': 24 * 60},
      {'method': 'popup', 'minutes': 10},
    ],
  },
}
service.events().insert(calendarId=calendar_id, body=event).execute()
print(result)