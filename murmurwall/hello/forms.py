from django import forms
from hello.models import Word

class WordForm(forms.ModelForm):

    class Meta:
        model = Word


