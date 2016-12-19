from django import forms

class RejoindreForm(forms.Form):
    famille_id = forms.IntegerField(label='Famille')