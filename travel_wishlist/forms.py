from django import forms
from .models import Place

# This form is used to create or edit Place objects.
# It automatically generates form fields based on the Place model.

class NewPlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ['name', 'visited']
    