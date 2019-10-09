from django import forms
from api.models import houseDetails,area,areaQuantity,quality,userConsumption
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):

    class Meta():
        model = User
        fields = ('username','first_name','last_name','password','email')

class areaForm(forms.ModelForm):

    class Meta():
        model = area
        fields = ('areaName',)

class houseForm(forms.ModelForm):

    class Meta():
        model = houseDetails
        fields = ('house_no','street_name','pincode',)

