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
