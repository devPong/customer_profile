
from django.urls import path
from . import views
# from . import views
# from .address_api import get_province_all

app_name = 'web_app'


urlpatterns = [
    

    path('/cm',views.contact_management,name="contactManagement"),

    # path('AllStamp',views.AllStamp,name="AllStamp"),

]