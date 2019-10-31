from django.shortcuts import render
from api.models import houseDetails,area,areaQuantity,quality,userConsumption,Complain
from api.forms import UserForm,areaForm,houseForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils import timezone
from django.http import JsonResponse
from django.core import serializers
import random
# Create your views here.

"""
API CONFIGURATION

----------------->API FOR HARDWARE <----------------

-->api/hardware/userConsumption:
FOR HOUSE LEVEL WATER CONSUMPTION
https://aquapaywik.herokuapp.com/api/hardware/user?meter_id=12&quantity=21

meter_id must be same as that of house_no during registration

default = 12

-->api/hardware/areaRequest:
FOR AREA LEVEL WATER CONSUMPTION
https://aquapaywik.herokuapp.com/api/hardware/area?areaid=AREA1&quantity=100
use areaid = AREA1 OR AREA2

-->api/hardware/quality:
API FOR QUALITY   
https://aquapaywik.herokuapp.com/api/hardware/quality?quality=10



-------> SOFTWARE FOR USER <---------

-->api/software/signup

https://aquapaywik.herokuapp.com/api/software/signup?username=ranjanravi25&email=ravi25@gmail.com&password=1234&firstname=Ravi&lastname=Singh&street=164vip&houseno=10&pincode=12345

Return type boolean {result:1} 1->success
                               0->username already in use(email will be added in next update)
---> api/software/login

https://aquapaywik.herokuapp.com/api/software/login?username=ranjanravi25&password=1234

Return type boolean {result:1,admin = 0/1,}
                            Result ==    1->success
                                         0->incorrect username or password(email will be added in next update)
                            Admin ==   1-> User is admin
                                       0->User not a admin    

-->api/software/water(Returns Water Consumption)

https://aquapaywik.herokuapp.com/api/software/waterconsumed?username=ranjanravi25

Return type float {result:AMOUNT OF WATER CONSUMED} 


-->api/software/Complain

FILE WATER COMPLAIN

https://aquapaywik.herokuapp.com/api/software/complain?username=ranjan&complain=qwertyuighbnbnhnhjm&complainid="Water Quality"

Return type boolean {result:1} 1->success

--> api/software/viewConsumption

VIEW CONSUMPTION

http://aquapaywik.herokuapp.com/api/software/viewconsumption?params="AREA1"
                    params --> "all"/"AREA1"/"AREA2"


--> api/software/showuser
http://aquapaywik.herokuapp.com/api/software/showuser

Return  {result:"user details"} 


--> api/software/showquality
http://aquapaywik.herokuapp.com/api/software/showquality

Return  {result:"  "} 


--> api/software/showcomplains
http://aquapaywik.herokuapp.com/api/software/showcomplains

Return  {result:"  "}

--> api/software/paytmcall
http://aquapaywik.herokuapp.com/api/software/paytmcall




"""
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#---------------------HARDWARE APIS-----------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------


def userConsumptionN(request):
    house = request.GET.get('meter_id')
    
    amount = request.GET.get('quantity')
    
    d = houseDetails.objects.get(house_no=house)
   
    c = userConsumption(user = d.user,consumption = amount)
    c.save()
    return JsonResponse({'result':1})
    

def areaRequest(request):
    area_id = request.GET.get('areaid')
    quantityWater = request.GET.get('quantity')
    
    d = area.objects.get(areaid=area_id)
    c = areaQuantity(areaN = d,quantity = quantityWater)
    c.save()
    return JsonResponse({'result':1})


def qualityN(request):
    qualityOfWater = request.GET.get('quality')
    
    d = quality(quality = qualityOfWater)
    d.save()
    return JsonResponse({'result':1})


#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#---------------------USER APIS-----------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------






def index(request):
    form = UserForm()
    areaf = areaForm()
    house = houseForm()

    if request.method == "POST":

        form = UserForm(request.POST)
        house = houseForm(request.POST)    
        if form.is_valid() and house.is_valid():
           user = form.save(commit=True)
           house_add = house.save(commit=False)
           house_add.user = user
           house_add.save()
            

    return render(request,"index.html",{'form':form,'area': areaf,'house':house})    


def signup(request):
    userName = request.GET.get('username')
    eMail = request.GET.get('email')
    firstname = request.GET.get('firstname')
    lastname = request.GET.get('lastname')
    Password = request.GET.get('password')
    House_no = request.GET.get('houseno')
    street = request.GET.get('street')
    Pincode = request.GET.get("pincode")
    aarea = request.GET.get("areaid")
    
    
    check = User.objects.filter(username = userName)
    checkEmail = User.objects.filter(email = eMail)
    checkHouse = houseDetails.objects.filter(house_no=House_no)
    if len(check) > 0:
        
            return JsonResponse({'result':0,'message':'Username already exist'})
    
    elif len(checkEmail) > 0:

            return JsonResponse({'result':0,'message':'Email address already exist'})


    elif len(checkHouse) > 0:
             return JsonResponse({'result':0,'message':'House already registered'})
    else:
        print(street)
        user1 = User.objects.create_user(username = userName, email=eMail, password=Password, first_name = firstname , last_name = lastname)
        area1 = area.objects.get(areaid=aarea)
        house_add = houseDetails(house_no = House_no,street_name =street,pincode =Pincode,Area=area1)
        house_add.user = user1
        house_add.save()
          
        # Return 1
        return JsonResponse({'result':1,'message':'success'})


def login(request):
    userName = request.GET.get('username')
    Password = request.GET.get('password')
    

    user1 = authenticate(username=userName, password=Password)


    if user1 is not None:
            admin = 0 
            house = houseDetails.objects.get(user = user1)
            if(house.admin == 1):
                admin = 1

            return JsonResponse({'result':1,'username':user1.username,'email':user1.email,'firstname':user1.first_name,
                                'lastname':user1.last_name,'house_no':house.house_no,'street_name':house.street_name,'pincode':house.pincode,'admin':admin})
    else:
        return JsonResponse({'result':0})

def water(request):
    userName = request.GET.get('username')
    user1 = User.objects.get(username=userName)

    consumed = userConsumption.objects.filter(time__gte=timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0),user=user1)
    amount = 0.0

    for c in consumed:
        amount = amount+c.consumption

    return JsonResponse({'result':amount})

    
def complainss(request):
    userName = request.GET.get('username')
    complains = request.GET.get('complain')
    complainid1 = request.GET.get('complainid')



    user1 = User.objects.get(username=userName)

    complaint = random.randint(100,999) + random.randint(9999,10000) + user1.pk
    
    complaint = "COMP25"+str(complaint)


    print(complaint)
    comp = Complain(complain = complains,complainid = complainid1,complaintxn = complaint )
    comp.user = user1
    comp.save()    

    return JsonResponse({'result': 1})



def viewConsumption(request):
    params = request.GET.get('params')
    
    if params == "all":
        areaComplete = areaQuantity.objects.all()
        return_json = serializers.serialize("json", areaComplete)
        data = {"result": return_json}
        return JsonResponse(data)


    else:
        
        areaParam = userConsumption.objects.filter(areaid = params)
        return_json = serializers.serialize("json", areaParam)
        data = {"result": return_json}
        return JsonResponse(data)
 
    # houseWise = User.objects.all().values('username')
    
    


def showComplains(request):
        complains = Complain.objects.all()
        return_json = serializers.serialize("json", complains)
        data = {"result": return_json}
        return JsonResponse(data)
 
def showQuality(request):
        complains = quality.objects.all()
        return_json = serializers.serialize("json", complains)
        data = {"result": return_json}
        return JsonResponse(data)

def showUser(request):
        complains = User.objects.all()
        return_json = serializers.serialize("json", complains)
        data = {"result": return_json}
        return JsonResponse(data)

def paytmCall(request):
        username1 = request.object.post('username')
        am = request.object.post('TXN_AMOUNT')

        user1 = User.objects.get(username = username1)

        complaint = random.randint(100,999) + random.randint(9999,10000) + user1.pk
    
        txn = "TXN25"+str(complaint)

        transaction = tax(amount = am, txnid = txn)
        transaction.user = user1
        transaction.save()

        