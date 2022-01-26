from django import forms
from . import models
from authentication.models import User
from django.core.exceptions import ValidationError


class TicketForm(forms.ModelForm):
    """https://stackoverflow.com/questions/14336925/how-to-not-render-django-image-field-currently-and-clear-stuff"""
    image = forms.FileField(widget=forms.FileInput)

    class Meta:
        model = models.Ticket
        fields = ['title', 'description', 'image', ]


class ReviewForm(forms.ModelForm):
    choices = ((0, '0'),  (1, '1'), (2, '2'),  (3, '3'),  (4, '4'),  (5, '5'), )
    rating = forms.TypedChoiceField(widget=forms.RadioSelect, choices=choices, coerce=int, initial='0')

    class Meta:
        model = models.Review
        fields = ['headline', 'rating', 'body', ]


class UserFollowsForm(forms.Form):
    """
    Check that the followed user is different from current user.
    For that purpose request.user is passed to the form from the view follower_update method.
    The init method of the Form is redefined so as to accept another parameter.
    Check if followed user is already registered
    All that is done using a clean_username that is executed when the form is instantiated"""

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(UserFollowsForm, self).__init__(*args, **kwargs)

    username = forms.CharField(max_length=63, label='Username', required=True)
    add_followee = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    def clean_username(self):
        newuser = self.cleaned_data['username']
        if not User.objects.filter(username=newuser).exists():
            raise ValidationError("You can't follow unregistered users!")
        if newuser == self.user.username:
            raise ValidationError("You can't follow yourself!")
        return newuser


class DeleteFollowsForm(forms.Form):
    delete_followee = forms.BooleanField(widget=forms.HiddenInput, initial=True)
