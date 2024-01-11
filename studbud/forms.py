from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm


class myUserCreationForm(UserCreationForm):
    class Meta:
        model= User
        fields = ['name' ,'username' , 'email' , 'password1' , 'password2']

class roomForm(ModelForm):
    
    class Meta:
        model = room
        fields = '__all__'
        exclude = ['host' , 'participants']

class userForm(ModelForm):
    
    class Meta:
        model = User
        
        fields = ['avatar' ,'username' , 'email' ,'bio']
