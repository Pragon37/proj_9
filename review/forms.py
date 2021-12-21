from django import forms
from . import models

class TicketForm(forms.ModelForm):
    """https://stackoverflow.com/questions/14336925/how-to-not-render-django-image-field-currently-and-clear-stuff"""
    image = forms.FileField(widget=forms.FileInput)
    class Meta:
        model = models.Ticket
        fields = ['title', 'description', 'image',]

class ReviewForm(forms.ModelForm):
    choices = ( (0,'0'), (1,'1'),(2,'2'), (3,'3'), (4,'4'), (5,'5'), )

    rating = forms.TypedChoiceField( widget=forms.RadioSelect, choices=choices, coerce=int, initial='0')

    class Meta:
        model = models.Review
        fields = ['headline', 'rating', 'body',]
