from django import forms
from myapp.models import Post,Faq, Event
class HomeForm(forms.ModelForm):
    post = forms.CharField()
    class Meta:
        model = Post
        fields = ('post', )

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Faq
        fields = ('question', 'answer')

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('name', 'date', 'duration') 