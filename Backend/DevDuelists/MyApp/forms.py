from django import forms
from .models import Code

LANGUAGE_CHOICES = [
    ('cpp', 'C++'),
    ('c', 'C'),
    ('py', 'Python'),
]

class CodeSubmissionForm(forms.ModelForm):
    language = forms.ChoiceField(choices=LANGUAGE_CHOICES)
    
    class Meta:
        model = Code
        fields = ['language', 'code']
