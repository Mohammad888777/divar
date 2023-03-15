from django import forms
from .models import User


class SignUpForm(forms.ModelForm):

    phone_number=forms.CharField(max_length=200,required=True,label="شماره تلفن",)
    class Meta:
        fields=["phone_number"]
        model=User