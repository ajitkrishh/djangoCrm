from django.shortcuts import render,redirect,reverse
from django.views import generic 
from leads.models import Agent,UserProfile
from .forms import AgentModelForm
 # Create your views here.
from django.core.mail import send_mail
from .mixins import organisorandLoginRequiredMixin
import random
class AgentListView(organisorandLoginRequiredMixin,generic.ListView):
    template_name = "agents/agent_list.html"

    def get_queryset(self):
        try:
            request_organisation = self.request.user.userprofile
        except UserProfile.DoesNotExist:
            return None
        queryset = Agent.objects.filter(organisation = request_organisation)
        return queryset
        
class AgentCreateView(organisorandLoginRequiredMixin,generic.CreateView):
    template_name = "agents/agent_create.html"
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse("agent-list")
    def form_valid(self,form):
        user = form.save(commit = False)
        user.is_agent = True
        user.date_of_birth = form.cleaned_data['DOB']
        user.is_organisor = False
        user.set_password(f"{random.randint(0,1000000)}")
        user.save()
        Agent.objects.create(
            user = user,
            organisation=self.request.user.userprofile,

        )
        send_mail(
            subject = "A Agent is Created",
            message = "Go to the site ",
            from_email = "test@agent.com",
            recipient_list =["agent@created.com"]
        )
        return super(AgentCreateView , self).form_valid(form)
        # return None

   
class AgentDetailView(organisorandLoginRequiredMixin,generic.DetailView):
    template_name = "agents/agent_detail.html"
    queryset = Agent.objects.all()

    
class AgentUpdateView(organisorandLoginRequiredMixin,generic.UpdateView):

    template_name = "agents/agent_update.html"
    form_class = AgentModelForm
    queryset = Agent.objects.all()

    def get_success_url(self):
            return reverse("agent-list")
 

class AgentDeleteView(organisorandLoginRequiredMixin,generic.DeleteView):
    template_name = "agents/agent_delete.html"
    queryset = Agent.objects.all()


    def get_success_url(self):
            return reverse("agent-list")
