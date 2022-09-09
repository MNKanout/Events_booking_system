from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from .models import Member

# class NumberInput(Input):
class TelInput(forms.widgets.Input):
    input_type = 'tel'

class DateInput(forms.DateInput):
    input_type = 'date'

class RegisterForm(forms.ModelForm):
    confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))

    error_css_class = 'error'
    required_css_class = 'required'

    class Meta:
        model = Member
        fields = ['username','first_name','last_name','birthday','email','password']
        labels = {'username':'Phone Number'}
        widgets = {
            'first_name':forms.TextInput(attrs={'class':'form-control'}),
            'last_name':forms.TextInput(attrs={'class':'form-control'}),
            'birthday':DateInput(attrs={'class':'form-control'}),
            'username':TelInput(attrs={'class':'form-control','placeholder':'+47 XX-XXX-XXX'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'password':forms.PasswordInput(attrs={'class':'form-control'})
            }


    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError({"confirm_password":"Password and Confirm password fields did not match."})
        else:
            validate_password(cleaned_data["password"])
            cleaned_data["password"] = make_password(cleaned_data["password"])



class LoginForm(AuthenticationForm):
    error_messages = {
        'invalid_login': (
            "Invalid phone number or password"),
        'inactive': ("This account is inactive."),
    }
    username = forms.CharField(label="Phone Number",widget=TelInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))







