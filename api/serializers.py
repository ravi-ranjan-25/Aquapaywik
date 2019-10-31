from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import Complain,Tax

class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['pk','username','first_name','last_name','email']

class complainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complain
        fields = '__all__'

class transactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tax
        fields = '__all__'
