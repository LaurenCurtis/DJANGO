from django import forms

from .models import Topic 
from .models import Entry
class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['text']
        labels = {'text':''}

class EntryForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields =['text']
        labels = {'text':''}