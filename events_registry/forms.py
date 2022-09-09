from django.forms import ModelForm
from django import forms
from .models import Event


class DateInput(forms.DateInput):
    input_type = 'date'


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['name','start_date','start_time','end_date','end_time','max_number_of_participants']
        labels = {'name':'Event name','start_date':'Starting date','start_time':'Starting Time','end_date':'Ending Date','end_time':'Ending time','max_number_of_participants':'Total number of participants'}

        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control','placeholder':'Fredagsbønn'}),
            'start_date': DateInput(attrs={'class':'form-control'}),
            'start_time': forms.TimeInput(attrs={'type':'time','class':'form-control'}),
            'end_date': DateInput(attrs={'class':'form-control'}),
            'end_time': forms.TimeInput(attrs={'type':'time','class':'form-control'}),
            'max_number_of_participants': forms.NumberInput(attrs={'class':'form-control','max':1000,'placeholder':60}),
        }

