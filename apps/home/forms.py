from tkinter.tix import Select
from django.db import models
from django.forms import ModelForm
from .models import * 
from django import forms


class AddPatientForm(ModelForm):
    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'birthday', 'email', 'gender', 'address', 'state', 'city', 'zip_code', 'phone']
       

class UpdatePatientForm(ModelForm):
    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'birthday', 'email', 'gender', 'address', 'state', 'city', 'zip_code', 'phone']
       


class UpdatePrediction(ModelForm):
    class Meta:
        model = Prediction
        fields = ['model_feedback'] 
   