from django.db import models

# Create your models here.


class Book(models.Model):
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

class Post(models.Model):
    post = models.CharField(max_length = 500)

class Faq(models.Model):
    question = models.CharField(max_length=200)
    answer = models.CharField(max_length=300)

class Event(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateTimeField('date taking place')
    duration = models.IntegerField('duration of event')
