#!/usr/bin/python
# -*- coding:Utf-8 -*-

from django import forms

class RejoindreForm(forms.Form):
    famille_id = forms.IntegerField(label='Famille', required=False)
    ajout = forms.CharField(label='ajout')