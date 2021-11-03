from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import date
from django.db.models.signals import post_save
# Create your models here.
class User(AbstractUser):
    is_organisor = models.BooleanField(default = True)
    is_agent = models.BooleanField(default = False)

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete = models.CASCADE)

    def __str__(self):
        return self.user.username

class Lead(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    organisation = models.ForeignKey(UserProfile ,  on_delete = models.CASCADE)
    date_of_birth = models.DateField(default=date.today)
    discription = models.TextField(default="None")
    agent = models.ForeignKey("Agent",null = True,blank = True, on_delete = models.SET_NULL)
    category = models.ForeignKey("Category",related_name="leads",null = True,blank = True, on_delete = models.SET_NULL)

    def __str__(self):
        return '%s %s %s'%(self.first_name ,self.organisation,self.agent)


class Agent(models.Model):
    user = models.OneToOneField(User,on_delete = models.CASCADE)
    organisation = models.ForeignKey(UserProfile ,  on_delete = models.CASCADE)
    date_joined = models.DateTimeField(default=timezone.now)
    date_of_birth = models.DateField()
    def __str__(self):
        return self.user.username

class Category(models.Model):
    name = models.CharField(max_length=15)
    organisation = models.ForeignKey(UserProfile ,  on_delete = models.CASCADE)
    def __str__(self):
        return self.name


def post_user_created_signal(sender , instance , created,**kwargs):
    if created:
        UserProfile.objects.create(user = instance)

post_save.connect(post_user_created_signal,sender = User)