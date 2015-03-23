__author__ = 'emilcieslar'

from django import forms
from django.contrib.auth.models import User

from representME.models import UserProfile, Comment

# Using this we will check for valid zipcode (assuming
# that no one will enter non-scottish zipcode)
from localflavor.gb.forms import GBPostcodeField


# Customizing registration form
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}), label="", help_text="")
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Email address'}), label="", help_text="")
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}), label="", help_text="")

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

# Customizing registration form continue..
class UserProfileForm(forms.ModelForm):
    postcode = GBPostcodeField(widget=forms.TextInput(attrs={'placeholder': 'Postcode'}), label="", help_text="")

    class Meta:
        model = UserProfile
        fields = ('postcode',)

# Form for commenting a law
class LawCommentForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Add your message here...'}), label="",
                           help_text="")

    class Meta:
        model = Comment
        fields = ('text',)