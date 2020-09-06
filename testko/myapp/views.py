from django.shortcuts import render
from difflib import SequenceMatcher
from django.http import HttpResponse
from .models import Book, Post, Faq, Event
from django.views.generic import TemplateView
from myapp.forms import HomeForm, QuestionForm, EventForm
from django.shortcuts import render, redirect
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from dateutil import parser
from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from datetime import datetime, timedelta
import pickle
import os

ev = ''

# Create your views here.
class EventView(TemplateView):
    template_name = 'design.html'

    def get(self, request):
        form = EventForm()
        return render(request, self.template_name, {'form':form})
    
    def post(self, request):
        form = EventForm(request.POST)
        form.save()
        return render(request, self.template_name, {'form':form})

class FaqView(TemplateView):
    template_name = 'design2.html'

    def get(self, request):
        form = QuestionForm()
        return render(request, self.template_name, {'form':form})
    
    def post(self, request):
        form = QuestionForm(request.POST)
        form.save()
        return render(request, self.template_name, {'form':form})

class HomeView(TemplateView):
    template_name = 'design3.html'
    def get(self, request):
        return render(request, self.template_name)

def ViewData(request, post_name):
    post_id = Post.objects.get(post = post_name)
    return HttpResponse(post_id)


def book_by_id(request, book_id):
    book = Book.objects.get(pk = book_id)
    return HttpResponse(f"Book: {book.title}, published on {book.pub_date}")

@csrf_exempt
#@require_POST
def webhook_endpoint(request):
    jsondata = request.body.decode('utf-8')
    print(jsondata)
    data = json.loads(jsondata)
    q = data['queryResult']['queryText']
    siz = Faq.objects.all().count()
    speech = 'Sorry, I cannot answer that.'

    if data['queryResult']['intent']['displayName'] == 'Default Fallback Intent':
        for a in Faq.objects.all():
            if (SequenceMatcher(None, q, a.question).ratio() >= 0.75 ):
                speech = a.answer    

    if data['queryResult']['intent']['displayName'] == 'getEmail':
        email = data['queryResult']['outputContexts'][0]['parameters']['email']
        fName = '../' + email +'.pkl'
        if os.path.exists(fName):
            speech = 'Got it! ' + data['queryResult']['outputContexts'][0]['parameters']['email']
        else:
            speech = "Sorry, please register your email with the company."

    if data['queryResult']['intent']['displayName'] == 'eventIntent':
        speech = 'Sorry, there is no such event.'
        for a in Event.objects.all():
            if a.name in q:
                ev = a.name
                start = a.date
                end = a.date + timedelta(hours = a.duration)
                day = parser.parse(str(a.date)[:10]).strftime("%A")
                #speech = a.name + ' is on ' + day + ', ' + str(a.date)[:10] + ', from ' + str(a.date)[11:16] + ' to ' + str(int(str(a.date)[11:13]) + a.duration) + str(a.date)[13:16] + '. Would you like to add it to your calendar?'
                speech = a.name + ' is on ' + day + ', ' + str(a.date)[:10] + ', from ' + start.strftime("%H:%M") + ' to ' + end.strftime("%H:%M") + '. Would you like to add it to your calendar?'
                email = data['queryResult']['outputContexts'][0]['parameters']['email']
                fName = '../' + email +'.pkl'
                if os.path.exists(fName):
                    credentials = pickle.load(open('../' + email +'.pkl', 'rb'))
                    service = build("calendar", "v3", credentials = credentials)
                    result = service.calendarList().list().execute()
                    calendar_id = result['items'][3]['id']
                    event = {
                        'summary': a.name,
                        'location': 'TBD',
                        'description': '',
                        'start': {
                        'dateTime': start.strftime("%Y-%m-%dT%H:%M:%S"),
                        'timeZone': 'Europe/Bucharest',
                    },
                    'end': {
                    'dateTime': end.strftime("%Y-%m-%dT%H:%M:%S"),
                    'timeZone': 'Europe/Bucharest',
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
    rep = {
            "speech": speech,
            "displayText": speech,
            #"data": {},
            #"contextOut": [],
            "source": "BankRates",
            "fulfillmentText":speech
        }
    return JsonResponse(rep)
