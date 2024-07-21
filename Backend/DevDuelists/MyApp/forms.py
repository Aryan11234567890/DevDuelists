from django import forms
from .models import Code

class CodeSubmissionForm(forms.ModelForm):
    class Meta:
        model = Code
        fields = ['code']
        widgets = {
            'code': forms.Textarea(attrs={
                'rows': 20,
                'cols': 80,
                'placeholder': 'Write your code here...',
                'style': 'width: 100%; height: 400px; font-family: monospace; font-size: 14px; background-color: #282c34; color: #abb2bf; padding: 10px; border-radius: 4px; border: 1px solid #ddd;'
            }),
        }
