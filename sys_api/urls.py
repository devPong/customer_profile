
from django.urls import path
from .erp_api import contactERP
from .address_api import addressApi
from .contactApp_api import contactApi
from .personApp_api import personApi
# from . import views
# from .address_api import get_province_all

app_name = 'sys_api'


urlpatterns = [
    

    path('/province',addressApi.province_all,name="provinceAll"),
    path('/district',addressApi.district_withProvince,name="districtWithProvince"),
    path('/subdistrict',addressApi.subdistrict_withDistrict,name="subdistrictWithProvince"),
    path('/erpContact',contactERP.contact_all,name="erpContact"),
    
    path('/contactMG',contactApi.contact_mangement,name="contactManage"),
    path('/personMG',personApi.person_mangement,name="contactManage"),
    

    # path('AllStamp',views.AllStamp,name="AllStamp"),
    


]