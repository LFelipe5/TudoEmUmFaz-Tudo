from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title']
        widgets = {'title': forms.TextInput(attrs={'placeholder': 'What do you want to do?'})}


class ScrapeForm(forms.Form):
    url = forms.URLField(label='Public page URL', max_length=2048)
