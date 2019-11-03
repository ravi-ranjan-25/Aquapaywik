"""aquapaywik URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from api import views
from rest_framework import routers
from .views import UserListView,complainListView,transactionListView,qualityListView,homepageListView,walletListView,areaListView

# router = routers.DefaultRouter()
# router.register('users',views.UserListView , base_name="User")

urlpatterns = [
   
    path('hardware/user',views.userConsumptionN , name = "userConsumptionN"),
    path('hardware/area',views.areaRequest , name = "areaRequest"),
    path('hardware/quality',views.qualityN , name = "qualityN"),
    path('hardware/model',views.modelapi , name = "model"),


    path('hardware/',views.index , name = "index"),
    
    path('software/signup',views.signup , name = "use"),
    path('software/login',views.login , name = "log"),
    path('software/waterconsumed',views.water , name = "water"),
    path('software/complain',views.complainss , name = "comp"),
#   path('/show',include(router.urls)),

    path('software/viewconsumption',views.viewConsumption , name = "comp2"),
    path('software/showcomplains',complainListView.as_view(),name = "complain"),
    path('software/showquality',qualityListView.as_view(),name = "quality"),
    path('software/showuser',UserListView.as_view(),name = "use"),
    path('software/paytmcall',views.paytmCall,name = "paytmcall"),
    path('software/transaction',transactionListView.as_view(),name = "transaction"),
    path('software/estimated',views.estimated,name = "estimated"),
    path('software/pendingtax',views.pendingTax,name = "estimated1"),
    path('software/pendinguser',views.pendinguser,name = "estimated3"),
    path('software/homepage',homepageListView.as_view(),name = "homese"),
    
    path('software/pending',walletListView.as_view(),name = "homes2e"),
    path('software/areagraph',areaListView.as_view(),name = "homes22e"),
    path('software/viewprofile',views.viewprofile,name = "homes022e"),


]