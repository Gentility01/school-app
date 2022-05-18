
from pyexpat import model
from tkinter import Widget
from django import forms
from .models import SessionYearModel

class SessionForm(forms.ModelForm):
    session_start_year = forms.DateTimeField( input_formats=['%d/%m/%Y %H:%M'],
                    widget=forms.DateTimeInput(attrs={"class":"form-control datetimepicker-input ",
                                                      'data-target': '#datetimepicker1'}))
    session_end_year = forms.DateTimeField(widget=forms.TextInput(attrs={"class":"form-control", 'placeholder':'Enter Slug'}))
    class Meta:
        model = SessionYearModel
        fields = [
            'session_start_year',
            'session_end_year'
        ]