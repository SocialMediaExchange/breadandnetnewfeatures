from django import forms
from django.contrib.auth.models import User

THEMES_ChOICES = [
    ("ETHICAL TECH", "ETHICAL TECH"),
    ("DIGITAL AUTHORITARIANISM", "DIGITAL AUTHORITARIANISM"),
    ("RESISTANCE COMMUNITIES AND MOVEMENT BUILDING", "RESISTANCE COMMUNITIES AND MOVEMENT BUILDING"),
    ("POLICIES AND LAW", "POLICIES AND LAW"),
    ("KNOWLEDGE SHARING AND LEARNING", "KNOWLEDGE SHARING AND LEARNING")]

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
 
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)
    YEARS= [x for x in range(1940,2021)]
    birth_date= forms.DateField(label='What is your birth date?', 
    widget=forms.SelectDateWidget(years=YEARS))
    Theme_Select = forms.MultipleChoiceField(
        required=True,
        widget = forms.CheckboxSelectMultiple,
        choices = THEMES_ChOICES,
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',)
        # add new fields with checkboxes!!!

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords do not match.')
        return cd['password2']