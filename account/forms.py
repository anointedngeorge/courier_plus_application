from django import forms
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from authModel.models import AppAuthUser
from django.forms import fields


class userRegistrationForm(UserCreationForm):
    
    email = forms.EmailField(required=True)

    class Meta:
        model = AppAuthUser
        fields = ("username","first_name", "last_name", "email", "password1", "password2", "roles")

    
    def save(self, commit=True):

        try:
            user = super(userRegistrationForm, self).save(commit=False)
            user.email = self.cleaned_data['email']

            if commit:
                user.is_staff = True
                user.is_active = True
                user.save()
        
            return user

        except Exception as e:
            print(e)
