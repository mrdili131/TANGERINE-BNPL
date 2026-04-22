from django import forms
from .models import *

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['passport_serial','passport_pinfl','birth_date','income']