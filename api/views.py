from django.shortcuts import render
from api.models import houseDetails,area,areaQuantity,quality,userConsumption,Complain,Tax,wallet
from api.forms import UserForm,areaForm,houseForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils import timezone
from django.http import JsonResponse
from django.core import serializers
import random
from .serializers import userSerializer,complainSerializer,transactionSerializer,qualitySerializer,homepageSerializer,walletSerializer,areaSerializer,usercSerializer
from rest_framework.generics import ListAPIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
import datetime
import pytz
import os
import pickle
import joblib
import json
import numpy as np 
from sklearn import preprocessing 
import pandas as pd
import requests
 
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

# def addconsumption(meter_id,quantiy):
    


def userConsumptionN(request):
    house = request.GET.get('meter_id')
    
    amount = request.GET.get('quantity')
    
    d = houseDetails.objects.get(house_no=house)
    ar = d.Area
    
    Areaid = ar.areaid
    User1 = d.user
    e = wallet.objects.get(user=User1)   
    c = userConsumption(user = d.user,consumption = amount,areaid=Areaid)
    a = area.objects.get(pk = ar.id)


    e.consumption = e.consumption + float(amount)
    consumed = e.consumption

    price = 0
    if(consumed <= 80):
        price = consumed * 1.5
    elif consumed >= 80 and consumed <= 150:
        price = (80*1.5)+(consumed - 80)*2.5
    else:        
        # price = (2*0.10)+(3*0.12)+(consumed-5)*1.5
        price = (80*1.5) + (70*2.5) + (consumed - 150)*5

    
    Status = 0

    # if(consumed <= 20):
    #     Status = 0
    # elif(consumed >=30 and consumed <= 40):
    #     Status = 1
    # else:
    #     Status = 2
        
    
    e.amount = price
    a.consumed = a.consumed + float(amount)
    a.areastatus = Status
    a.save()
    e.save()
    c.save()


    return JsonResponse({'result':1,'amount':e.amount})
    

def areaRequest(request):
    area_id = request.GET.get('areaid')
    quantityWater = request.GET.get('quantity')
    
    d = area.objects.get(areaid=area_id)
    c = areaQuantity(areaN = d,quantity = quantityWater)
    
    c.save()
    


    return JsonResponse({'result':1})


def qualityN(request):
    qualityOfWater = request.GET.get('voltage')
    Ntu = request.GET.get('ntu')
    
    d = quality(voltage = qualityOfWater,ntu = Ntu)
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
        Wallet = wallet()
        Wallet.user = user1
        house_add.user = user1
        house_add.save()
        Wallet.save()          
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
                consumed = userConsumption.objects.filter(time__gte=timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0),user=user1)

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
    
    



#def showUser(request):
    
            # return_json = serializers.serialize("json", complains)
            # data = {"result": return_json}
            # return JsonResponse(data)

def paytmCall(request):
        username1 = request.GET.get('username')
        am = request.GET.get('TXN_AMOUNT')

        user1 = User.objects.get(username = username1)
        user2 = User.objects.get(username = 'admin')
        
        print(user2)
        complaint = random.randint(100,999) + random.randint(9999,10000) + user1.pk
    
        txn = "TXN25"+str(complaint)
        wall = wallet.objects.get(user=user2)
        wall1 = wallet.objects.get(user=user1)
        
        transaction = Tax(amount = am, txnid = txn,username=username1)
        transaction.user = user1
        wall1.amount=0
        wall.amount = wall.amount + float(am)
        wall.save()
        wall1.save()
        transaction.save()
        return JsonResponse({'result':1})


class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = userSerializer

class complainListView(ListAPIView):
    queryset = Complain.objects.all()
    serializer_class = complainSerializer

class transactionListView(ListAPIView):
    queryset = Tax.objects.all()
    serializer_class = transactionSerializer

class qualityListView(ListAPIView):
    queryset = quality.objects.all()
    serializer_class = qualitySerializer

class homepageListView(ListAPIView):
    queryset = Tax.objects.all()
    serializer_class = homepageSerializer

class walletListView(ListAPIView):
    queryset = wallet.objects.all()
    serializer_class = walletSerializer

class areaListView(ListAPIView):
    queryset = areaQuantity.objects.all()
    serializer_class = areaSerializer

class usercListView(ListAPIView):
    queryset = userConsumption.objects.all()
    serializer_class = usercSerializer



def modelapi(request):
    return JsonResponse({'result': 2})

def estimated(request):
    # print(consumed.time)
    param = request.GET.get('areaparam')
    username1 = request.GET.get('username')
    total = 0
    walle = 0
    if(username1 == 'none'):
        am = Tax.objects.all()
        user1 = User.objects.filter(username = 'admin')
        
        myDict = (request.GET).dict()
        df=pd.DataFrame(myDict, index=[0])
        answer=approvereject(ohevalue(df)).tolist()
        a = answer[0]
    
        for i in answer:   
            a = i 

        for a in am:
            if(a.user != user1):
                total = a.amount + total

        if(param == "all"):
            consumed = userConsumption.objects.all()
        else:
            consumed = userConsumption.objects.filter(areaid=param)
    else:
            user1 = User.objects.get(username=username1)
            Wallet = wallet.objects.get(user = user1)
            walle = Wallet.amount
            consumed = userConsumption.objects.filter(user__username = username1)

            myDict = (request.GET).dict()
            df=pd.DataFrame(myDict, index=[0])
            answer=house_approvereject(house_ohevalue(df)).tolist()
            # a = answer[0]
    
            for i in answer:
                a = i 

            
            

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
        
    query = area.objects.all()[0]
    query1 = area.objects.all()[1]
    
    if(param == "all"):
        i=i*2

    i=i+i*0.2

    week = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
    day1 = datetime.datetime.today().weekday()
    
    link = 'https://aquapaywik.herokuapp.com/api/model/predict?area=s&day='+week[day1]
    link1 = 'https://aquapaywik.herokuapp.com/api/model/predict?area=n&day='+week[day1]

   
    response = requests.get(link)
    response1 = requests.get(link1)
    
    mapdata = response.json()
    mapdata1 = response1.json()
    param1 = ['AREA1','AREA2']
    map1 = mapdata['result'] + 0.2*mapdata['result']
    map2 = mapdata1['result'] + 0.2*mapdata1['result']
    
    areapredict=[map1,map2]
    index = [0,1]

    
    consumed2 = userConsumption.objects.filter(areaid='AREA1')
    consumed3 = userConsumption.objects.filter(areaid='AREA2')

    todayConsumed1 = todayConsumed2 = 0
    
    for w in consumed2:
        if(today<w.time):
            todayConsumed1 = todayConsumed1 + w.consumption;
    
    for w in consumed3:
        if(today<w.time):
            todayConsumed2 = todayConsumed2 + w.consumption;
    

    tconsumed = [todayConsumed1,todayConsumed2]
    st=0
    areast = ['0','1']



    for z in index:
       
        consumed1 = userConsumption.objects.filter(areaid=param[z])
        predicts = areapredict[z]

        if(tconsumed[z]<= 0.8*predicts):
            st = 0
        elif tconsumed[z] > 0.8*predicts and tconsumed[z] <= predicts:
            st = 1
        else:
            st = 2    
        
        areast[z] = st

    
     
    ############################################USER MARKER######################################################


    h = [1,2,3,4]
    
    index = [0,1,2,3]

    housest = [0,0,0,0]
    uconsume = [0.0,0.0,0.0,0.0]
    for z in index:
        linkh = 'https://aquapaywik.herokuapp.com/api/model/house?house=house'+ str(h[z]) +'&day=' + week[day1]
        responseh = requests.get(linkh)
        pred = responseh.json()
        
        predicth = pred['result']

        houseD = houseDetails.objects.get(house_no=h[z])
        userpk = houseD.user

        getuser = userConsumption.objects.filter(user=userpk)

        t = 0.0
        st = 0
        for u in getuser:
            # t = getuser.consumption + t
            if(today<u.time):
                t = t + u.consumption;

        if(t <= 0.8*predicth):
            st = 0
        elif t > 0.8*predicth and t <= predicth:
            st = 1
        else:
            st = 2    

        housest[z] = st
        uconsume[z]=t



    return JsonResponse({'today':todayConsumed,'month':monthConsumed,'seven':sevenConsumed,'yesterday': yesterdayConsumed,'pending':total,
                        'userPending':walle,'area1':areast[0],'area2':areast[1],
                        'tommorrow':i,'month1':50,'month2':60,'month3':80,'month4':90,'month5':120,'month6':200,'house1':housest[0],'house2':housest[1],'house3':housest[2],'house4':housest[3],
                        'house1-qty':uconsume[0],'house2-qty':uconsume[1],'house3-qty':uconsume[2],'house4-qty':uconsume[3]})
    
        
        
    #tdelta = today - consumed.time 

def pendingTax(request):
    user1 = User.objects.filter(username = 'admin')
    
    
    am = wallet.objects.all()
    total = 0
    for a in am:
        if(a.user != user1):
            total = a.amount + total
    
    
   
    return JsonResponse({'pending':total})


def pendinguser(request):
    username1 = request.GET.get('username')
    
    user1 = User.objects.get(username=username1)
    Wallet = wallet.objects.get(user = user1)
    

    return JsonResponse({'result': Wallet.amount})

def viewprofile(request):
    username1 = request.GET.get('username')
    
    user1 = User.objects.get(username=username1)
    Wallet = wallet.objects.get(user = user1)
    house = houseDetails.objects.get(user = user1)
    area1 = house.Area
    return JsonResponse({'result':1,'username':user1.username,'email':user1.email,'firstname':user1.first_name,
                        'lastname':user1.last_name,'house_no':house.house_no,'street_name':house.street_name,'pincode':house.pincode,'area':area1.areaName,
                        'water_consumed':Wallet.consumption,'pending_tax':Wallet.amount})
  
def resolveComplain(request):
    get_id = request.GET.get('id')

    comp = Complain.objects.get(pk=get_id)
    comp.status = True

    comp.save()
    return JsonResponse({'result':1})  

def mapCall(request):
    area1 = 'AREA1'
    area2 = 'AREA2'
    week = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
    day1 = datetime.datetime.today().weekday()
    
    link = 'http://localhost:8000/api/model/predict?area=s&day='+week[day1]
    link1 = 'http://localhost:8000/api/model/predict?area=n&day='+week[day1]

   
    response = requests.get(link)
    response1 = requests.get(link1)
    
    mapdata = response.json()
    mapdata1 = response1.json()

    # mapdata1 = response1.join()
    area1 = mapdata['result'] + 0.2*mapdata['result']
    area2 = mapdata1['result']+ 0.2*mapdata1['result']

    print(area1)
    # query = area.objects.all()[0]
    # query1 = area.objects.all()[1]
    
    
    # return JsonResponse({'AREA1':query.areastatus,'AREA2':query1.areastatus})  

def predict(request):
    BASE_DIRS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model_dir= os.path.join(BASE_DIRS,'api/aquapaywik_ohe.pkl')
    print(model_dir)


def ohevalue(df):
    BASE_DIRS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model_dir= os.path.join(BASE_DIRS,'api/aquapaywik_ohe.pkl')
    ohe_col = joblib.load(model_dir)
    cat_columns=['day','area']
    df_processed = pd.get_dummies(df, columns=cat_columns)
    print(df_processed)
    newdict={}
    
    for i in ohe_col:
        if i in df_processed.columns:
    	    newdict[i]=df_processed[i].values
        else:
    	    newdict[i]=0
    
    newdf=pd.DataFrame(newdict)
    print(newdf)
    return newdf


def house_ohevalue(df):
    BASE_DIRS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model_dir= os.path.join(BASE_DIRS,'api/aquapaywik_house_ohe.pkl')
    ohe_col = joblib.load(model_dir)
    cat_columns=['day','house']
    df_processed = pd.get_dummies(df, columns=cat_columns)
    print(df_processed)
    newdict={}
    
    for i in ohe_col:
        if i in df_processed.columns:
    	    newdict[i]=df_processed[i].values
        else:
    	    newdict[i]=0
    
    newdf=pd.DataFrame(newdict)
    print(newdf)
    return newdf





# def approvereject(unit):
# 	try:
# 		mdl=joblib.load("/home/ravi/Desktop/Ravi/www/bengalathon/aquapaywik/api/aquapaywik_model.pkl")
# 		# scalers=joblib.load("/Users/sahityasehgal/Documents/Coding/DjangoApiTutorial/DjangoAPI/MyAPI/scalers.pkl")
# 		X=unit
#         X=np.array(unit)
#         X=X.reshape(1,-1)
# 		# y_pred=mdl.predict(X)
# 		# y_pred=(y_pred>0.58)
# 		newdf=pd.DataFrame(y_pred, columns=['quantity'])
# 		# newdf=newdf.replace({True:'Approved', False:'Rejected'})
# 		K.clear_session()
# 		return (newdf.values[0][0],X[0])
# 	except ValueError as e:
# 		return (e.args[0])


def approvereject(unit):
    try:
        BASE_DIRS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        model_dir= os.path.join(BASE_DIRS,'api/aquapaywik_model.pkl')
    
        mdl=joblib.load(model_dir)
        
        X=unit
        X=np.array(unit)
        X=X.reshape(1,-1)
        y_pred=mdl.predict(X)
        print(y_pred)
        newdf=pd.DataFrame(y_pred>0.58, columns=['quantity'])
        print(newdf)
        # K.clear_session()
        return y_pred
    except ValueError as e:
        return (e.args[0])


def house_approvereject(unit):
    try:
        BASE_DIRS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        model_dir= os.path.join(BASE_DIRS,'api/aquapaywik_house_model.pkl')
    
        mdl=joblib.load(model_dir)
        
        X=unit
        X=np.array(unit)
        X=X.reshape(1,-1)
        y_pred=mdl.predict(X)
        print(y_pred)
        newdf=pd.DataFrame(y_pred>0.58, columns=['quantity'])
        print(newdf)
        # K.clear_session()
        return y_pred
    except ValueError as e:
        return (e.args[0])




# def cxcontact(request):

# 				myDict = (request.GET).dict()
# 				df=pd.DataFrame(myDict, index=[0])
# 				answer=approvereject(ohevalue(df))
                
# 				# Xscalers=approvereject(ohevalue(df))[1]
# 				# print(Xscalers)
# 				# messages.success(request,'Application Status: {}'.format(answer))
                
# 	            # form=ApprovalForm()
# 				return json.dumps({'result':answer,})
# 	            # return render(request, 'myform/cxform.html', {'form':form})
#                 # return JsonResponse({'pending':total})

def cxcontact(request):
    myDict = (request.GET).dict()
    df=pd.DataFrame(myDict, index=[0])
    answer=approvereject(ohevalue(df)).tolist()
    # a = answer[0]
    
    for i in answer:
        a = i 
    return JsonResponse({'result':i})



def house_cxcontact(request):
    myDict = (request.GET).dict()
    df=pd.DataFrame(myDict, index=[0])
    answer=house_approvereject(house_ohevalue(df)).tolist()
    # a = answer[0]
    
    for i in answer:
        a = i 
    return JsonResponse({'result':i})
