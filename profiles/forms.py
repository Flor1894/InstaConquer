from django import forms

class FollowForm(forms.Form):
    profile_pk = forms.IntegerField(label="Idendtificador del usuario", widget=forms.HiddenInput())
    action  = forms.CharField(widget=forms.HiddenInput(), initial="follow")
    