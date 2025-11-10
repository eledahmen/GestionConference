# ConferenceApp/forms.py

from django import forms
from .models import Conference, submission
from django.utils import timezone


class ConferenceModel(forms.ModelForm):
    class Meta:
        model = Conference
        fields = ['name', 'description', 'location', 'theme', 'start_date', 'end_date']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'theme': forms.Select(attrs={'class': 'form-select'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = submission
        fields = ['title', 'abstract', 'keywords', 'paper', 'conference']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'abstract': forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
            'keywords': forms.TextInput(attrs={'class': 'form-control'}),
            'paper': forms.FileInput(attrs={'class': 'form-control'}),
            'conference': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.instance.user = user
            self.fields['conference'].queryset = Conference.objects.all()
        