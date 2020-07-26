

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


# from django.contrib.auth.tokens import default_token_generator



class UserSignUpForm(UserCreationForm):
    bio = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = ['first_name','last_name','bio','email','username','password1','password2']

class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(max_length=256,widget=forms.PasswordInput())




class UserProfileUpdateForm(forms.ModelForm):
    # bio = forms.CharField(max_length=50)
    class Meta:
        model = User
        fields = ['first_name']

    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].widget.attrs.update({'class': 'form-control'})





