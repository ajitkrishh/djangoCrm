from django import forms

from django.contrib.auth import get_user_model 
from django.contrib.auth.forms import UserCreationForm,UsernameField

User = get_user_model()

class AgentModelForm(forms.ModelForm):
    DOB = forms.DateField(widget=forms.SelectDateWidget(years = range(1900,2100)))
    
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
        ]
            
       