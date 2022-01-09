from django import forms


class AddVotingForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    description = forms.CharField(widget=forms.Textarea)
    vote_type = forms.ChoiceField(
        choices={
            (0, "Discrete"),
            (1, "1:N"),
            (2, "M:N"),
        }
    )
from django.contrib.auth.models import User


class UserForm(forms.Form):
    username = forms.CharField(max_length=100)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
