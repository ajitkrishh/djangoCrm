from django import forms
from .models import Lead,Agent,Category

from django.contrib.auth.forms import UserCreationForm,UsernameField
from django.contrib.auth import get_user_model

User = get_user_model()


class LeadModelForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = [
            "first_name", 
            'last_name',
            'date_of_birth',
            'discription',
            "agent",
            "category"
        ]
        widgets = {
            "date_of_birth":forms.SelectDateWidget(years = range(1900,2100)),
        }
       


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields =("username",)
        field_classes = {"username" : UsernameField}


class AssigAgentForm(forms.Form):
    agent = forms.ModelChoiceField(queryset = Agent.objects.none())

    def __init__(self, *args,**kwargs):
        request = kwargs.pop("request")

        agents = Agent.objects.filter(organisation= request.user.userprofile)
        super(AssigAgentForm,self).__init__(*args,**kwargs)
        self.fields['agent'].queryset = agents


