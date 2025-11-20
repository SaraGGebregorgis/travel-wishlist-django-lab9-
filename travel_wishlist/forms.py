from django import forms
from .models import Place
from django.forms import DateInput


# This form is used to create or edit Place objects.
# It automatically generates form fields based on the Place model.

class NewPlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ['name', 'visited']

# This form is used when a user wants to add notes, a photo,
# and the date they visited a place.
class TripReviewForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ('notes', 'date_visited', 'photo')
        widgets = {
            'date_visited': DateInput()
        }
    