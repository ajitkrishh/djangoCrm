from django.shortcuts import render,redirect,reverse
from django.views import generic 
from .forms import LeadModelForm,CustomUserCreationForm,AssigAgentForm
from .models import Lead, Agent,Category

from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from agents.mixins import organisorandLoginRequiredMixin
from django.db.models import Count
# Create your views here.



class LandingPageView(generic.TemplateView):
    template_name = "landing.html"


class SignupView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse("login")


class LeadListView(LoginRequiredMixin,generic.ListView):
    template_name = "leads/lead_list.html"
    def get_queryset(self):
        usr = self.request.user
        if usr.is_organisor:
            queryset = Lead.objects.filter(organisation = usr.userprofile,agent__isnull = False)
        else:
            queryset = Lead.objects.filter(organisation = usr.agent.organisation,agent__isnull = False)
            queryset = queryset.filter(agent__user = usr)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(LeadListView,self).get_context_data(**kwargs)
        print(**kwargs)
        usr = self.request.user

        if usr.is_organisor:
            queryset = Lead.objects.filter(
                organisation = usr.userprofile,
                agent__isnull = True
                )
            context.update({
                "unassigned_leads": queryset,
            })
            return context

class LeadCreateView(organisorandLoginRequiredMixin,generic.CreateView):
    template_name = "leads/lead_create.html"
    form_class = LeadModelForm

    def get_success_url(self):
            return reverse("lead-list")

    def form_valid(self,form):
        lead = form.save(commit = False)
        lead.organisation = self.request.user.userprofile
        lead.save()
        send_mail(
            subject = "A lead is Created",
            message = "Go to the site ",
            from_email = "test@Lead.com",
            recipient_list =["lead@created.com"]
        )
        return super(LeadCreateView , self).form_valid(form)

class LeadDetailView(organisorandLoginRequiredMixin,generic.DetailView):
    template_name = "leads/lead_detail.html"
    def get_queryset(self):
        usr = self.request.user
        if usr.is_organisor:
            queryset = Lead.objects.filter(organisation = usr.userprofile)
        else:
            queryset = Lead.objects.filter(organisation = usr.agent.organisation)
            queryset = queryset.filter(agent__user = usr)
        return queryset


class LeadUpdateView(organisorandLoginRequiredMixin,generic.UpdateView):
    template_name = "leads/lead_update.html"
    form_class = LeadModelForm
    def get_queryset(self):
        usr = self.request.user
        queryset = Lead.objects.filter(organisation = usr.userprofile)
        return queryset

    def get_success_url(self):
            return reverse("lead-list")
 
class LeadDeleteView(organisorandLoginRequiredMixin,generic.DeleteView):
    template_name = "leads/lead_delete.html"
    def get_queryset(self):
        usr = self.request.user
        queryset = Lead.objects.filter(organisation = usr.userprofile)
        return queryset


    def get_success_url(self):
        return reverse("lead-list")

class AssignAgenttoLead(organisorandLoginRequiredMixin,generic.FormView):
    template_name = "leads/assign_agent.html"
    form_class = AssigAgentForm

    def get_form_kwargs(self,**kwargs):
        kwargs = super(AssignAgenttoLead,self).get_form_kwargs(**kwargs)
        kwargs.update({
            "request":self.request
        })
        return kwargs


    def form_valid(self, form):
        agent = form.cleaned_data["agent"]
        lead = Lead.objects.get(id = self.kwargs["pk"])
        lead.agent = agent
        lead.save()
        return super(AssignAgenttoLead,self).form_valid(form)

    def get_success_url(self):
        return reverse("lead-list")

class CategoryView(LoginRequiredMixin,generic.ListView):
    template_name = "leads/category/category_list.html"
    def get_queryset(self):
        usr = self.request.user
        if usr.is_organisor:
            queryset = Category.objects.filter(organisation = usr.userprofile)
        else:
            queryset = Category.objects.filter(organisation = usr.agent.organisation)
        return queryset

    def get_context_data(self,**kwargs):
        usr = self.request.user
        if usr.is_organisor:
            queryset = Lead.objects.filter(organisation = usr.userprofile)
        else:
            queryset = Lead.objects.filter(organisation = usr.agent.organisation)

        context = super(CategoryView,self).get_context_data(**kwargs)
        category_list = context['category_list']
        cat_count= []
        for i in category_list.values():
            cat_count.append(queryset.filter(category=i["id"]).count())

        print(cat_count)
        context.update({
            "object_list":zip(category_list,cat_count),
            "unassigned_lead_count" : queryset.filter(organisation__isnull = True).count()
        })
        return context

class CategoryDetailView(LoginRequiredMixin,generic.DetailView):
    template_name = "leads/category/category_detail.html"

    def get_queryset(self):
        usr = self.request.user
        
        if usr.is_organisor:
            queryset = Category.objects.filter(organisation = usr.userprofile)
        else:
            queryset = Category.objects.filter(organisation = usr.agent.organisation)
        return queryset

    def get_context_data(self,**kwargs):
        usr = self.request.user
        context = super(CategoryDetailView,self).get_context_data(**kwargs)
        if usr.is_organisor:
            queryset = Lead.objects.filter(category=context["object"] ,organisation = usr.userprofile )
        else:
            queryset = Lead.objects.filter(organisation = usr.agent.organisation,category=context["object"])
        context.update({
            "req_leads" : queryset
        })
        return context
