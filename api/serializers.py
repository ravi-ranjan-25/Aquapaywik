from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import Complain,Tax,quality,userConsumption,wallet,areaQuantity,

class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['pk','username','first_name','last_name','email']



class complainSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField('Complain')
    
    class Meta:
        model = Complain
        fields = '__all__'

    def Complain(self,wall): 
         user1 = wall.user.username
         return user1

class usercSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField('Complain')
    
    class Meta:
        model = Complain
        fields = '__all__'

    def Complain(self,wall): 
         user1 = wall.user.username
         return user1


class transactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tax
        fields = '__all__'

class areaSerializer(serializers.ModelSerializer):
    class Meta:
        model = areaQuantity
        fields = '__all__'


class qualitySerializer(serializers.ModelSerializer):
    class Meta:
        model = quality
        fields = '__all__'

class walletSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField('Wallet')
    
    class Meta:
        model = wallet
        fields = '__all__'

    def Wallet(self,wall): 
         user1 = wall.user.username
         print(user1)
         return user1

class homepageSerializer(serializers.ModelSerializer):
    my_field = serializers.SerializerMethodField('tax')
    
    
    class Meta:
            model = Tax
            fields = ['my_field',]

    def tax(self,foo):
        username1 = self.context['request'].GET['username']

        param = None
       
        request = self.context.get("request")
        if request and hasattr(request, "username"):
            username1 = request.username
        print(username1)
        if(username1 == 'none'):
            if(param == "all"):
                consumed = userConsumption.objects.all()
            else:
                consumed = userConsumption.objects.filter(areaid=param)
        else:
                consumed = userConsumption.objects.filter(user__username = username1)
        

        day1 = datetime.datetime.now(tz = pytz.UTC)
        today = day1.replace(hour=0, minute=0, second=0, microsecond=0)
        
        tdelta = datetime.timedelta(days = 7)
        tdelta1 = datetime.timedelta(days = 1)

        month = day1.replace(day=1,hour=0, minute=0, second=0, microsecond=0)
        seven = (day1 - tdelta)
        yesterday = (day1 - tdelta1)

        
        todayConsumed = monthConsumed = sevenConsumed = yesterdayConsumed = 0

        for c in consumed:
            if(today<c.time):
                todayConsumed = todayConsumed + c.consumption;
                

            if(c.time>month):
                monthConsumed = monthConsumed + c.consumption;

            if(c.time>seven):
                sevenConsumed = sevenConsumed + c.consumption;

            if c.time>yesterday and c.time<today:
                yesterdayConsumed = yesterdayConsumed + c.consumption;
            
        
        return foo.response == {'today':todayConsumed,'month':monthConsumed,'seven':sevenConsumed,'yesterday': yesterdayConsumed}

        