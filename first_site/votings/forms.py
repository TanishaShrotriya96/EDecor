# -*- coding: utf-8 -*-
from django import forms

class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file',
    )
    breadth = forms.CharField(
    	 widget=forms.TextInput(attrs={'type':'numeric'}),
     	 label=('breadth'), 
    	 required=True)
    length = forms.CharField(
    	 widget=forms.TextInput(attrs={'type':'numeric'}),
     	 label=('length'), 
    	 required=True)
