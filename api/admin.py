from django.contrib import admin
from api.models import houseDetails,area,areaQuantity,quality,userConsumption,Complain,wallet,Tax
# Register your models here.

admin.site.register(houseDetails)
admin.site.register(area)
admin.site.register(areaQuantity)
admin.site.register(quality)
admin.site.register(userConsumption)
admin.site.register(Complain)
admin.site.register(Tax)
admin.site.register(wallet)


