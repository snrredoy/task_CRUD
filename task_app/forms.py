from django import forms
from .models import Task

class SearchForm(forms.Form):
    title = forms.CharField()

class AddTaskForm(forms.ModelForm):
    class Meta:
        model= Task
        # field='__all__'
        fields=['title', 'description','completed']

    description = forms.CharField()