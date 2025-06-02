from django.contrib import admin
from django.urls import path
from . import views

app_name = 'wrtonline'


urlpatterns = [

    path('',views.homeWarranty,name="homeWarranty"),
    path('searchWarranty',views.searchWarranty,name="searchWarranty"),
    path('registersWarranty',views.registersWarranty,name="registersWarranty"),
    path('form_warranty',views.form_warranty,name="form_warranty"),
    path('find_provinces/', views.find_provinces, name='find_provinces'),
    path('find_districts', views.find_districts, name='find_districts'),
    path('find_subdistricts', views.find_subdistricts, name='find_subdistricts'),
    path('find_zipcode', views.find_zipcode, name='find_zipcode'),
    path('find_carbrand', views.find_carbrand, name='find_carbrand'),
    path('find_carmodel', views.find_carmodel, name='find_carmodel'),
    # path('find_gender', views.find_gender, name='find_gender'),
    path('find_provinces_contact', views.find_provinces_contact, name='find_provinces_contact'),
    path('find_contact_province', views.find_contact_province, name='find_contact_province'),

    path('find_group_front', views.find_group_front, name='find_group_front'),
    path('find_group_around', views.find_group_around, name='find_group_around'),
    path('find_group_another', views.find_group_another, name='find_group_another'),
    path('find_product_front', views.find_product_front, name='find_product_front'),
    path('find_product_around', views.find_product_around, name='find_product_around'),
    path('find_product_another', views.find_product_another, name='find_product_another'),
    
    path('update_warranty', views.update_warranty, name='update_warranty'),
    
    # path('previews_warranty', views.previews_warranty, name='previews_warranty'),
    path('warranty_print', views.warranty_print, name='warranty_print'),
    path('warranty_download', views.warranty_download, name='warranty_download'),
    path('form_warranty_views', views.form_warranty_views, name='form_warranty_views'),
    path('showdata_wrt', views.showdata_wrt, name='showdata_wrt'),
    path('showdata_wrt_list', views.showdata_wrt_list, name='showdata_wrt_list'),
    
    path('notFound_page', views.notFound_page, name='notFound_page'),
    path('cannotSave_page', views.cannotSave_page, name='cannotSave_page'),
    path('cannotSearch_page', views.cannotSearch_page, name='cannotSearch_page'),
    path('errorImage_page', views.errorImage_page, name='errorImage_page'),
]