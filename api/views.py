from django.shortcuts import render
from api.models import houseDetails,area,areaQuantity,quality,userConsumption,Complain
from api.forms import UserForm,areaForm,houseForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils import timezone
from django.http import JsonResponse
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

https://aquapaywik.herokuapp.com/api/software/slogin?username=ranjanravi25&password=1234

Return type boolean {result:1} 1->success
                               0->incorrect username or password(email will be added in next update)


-->api/software/water(Returns Water Consumption)

https://aquapaywik.herokuapp.com/api/software/waterconsumed?username=ranjanravi25

Return type float {result:AMOUNT OF WATER CONSUMED} 


-->api/software/Complain

FILE WATER COMPLAIN

https://aquapaywik.herokuapp.com/api/software/complain?username=ranjan&complain=qwertyuighbnbnhnhjm

Return type boolean {result:1} 1->success
                               


"""


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

    check = User.objects.filter(username = userName)

    if len(check) > 0:
        
            return JsonResponse({'result':0})

    else:
        user1 = User.objects.create_user(username = userName, email=eMail, password=Password, first_name = firstname , last_name = lastname)
        house_add = houseDetails(house_no = House_no,street_name =street,pincode =Pincode)
        house_add.user = user1
        house_add.save()
          
        # Return 1
        return JsonResponse({'result':1})


def login(request):
    userName = request.GET.get('username')
    Password = request.GET.get('password')
    
    user = authenticate(username=userName, password=Password)
    if user is not None:

            return JsonResponse({'result':1})
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

    user1 = User.objects.get(username=userName)

    comp = Complain(complain = complains)
    comp.user = user1
    comp.save()    

    return JsonResponse({'result': 1})

