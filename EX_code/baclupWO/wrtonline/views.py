from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connections
from .previews_print import showWarannty
from .download_warranty import downloadWarannty
import datetime
import json
import requests
import urllib.request
import base64
from django.core.files.base import ContentFile
from PIL import Image
import io 
from core.settings import API_Link

#ฟังก์ชันแปลงวันเดือนปีเป็นพ.ศ.ไปแสดง
def convert_date_to_thai_format(date_str):
    if not date_str:
        return None 
    try:
        date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d')
        thai_year = date_obj.year + 543
        formatted_date = date_obj.strftime(f'%d/%m/{thai_year}')
        return formatted_date
    except ValueError:
        return None
    
def homeWarranty(request):
    #เก็บข้อมูลของการกดยินยอม
    
    return render(request,'home_warranty.html')

def searchWarranty(request):
 
    
    return render(request,'form/search_warranty.html')


@csrf_exempt
def form_warranty_views(request):
    url2 = API_Link + "/erp_get/wNumberFinder"
    
    if request.method == 'POST':
        data2 = {
            'brand_wrt' : request.POST.get('brand_wrt'),
            'find_method' : request.POST.get('find_method'),
            'number_wrt' : request.POST.get('number_wrt'),
            'cust_firstname' : request.POST.get('cust_firstname'),
            'cust_lastname' : request.POST.get('cust_lastname'),
            'car_data' : request.POST.get('car_data'),
            'cardetail_condition' : request.POST.get('cardetail_condition')   
        }
        # print(data2)

        response2 = requests.post(url2, data=data2)

        find_method = request.POST.get('find_method')
        brand_wrt= request.POST.get('brand_wrt')
        number_wrt = request.POST.get('number_wrt')

        if response2.status_code == 200:
            api_result2 = response2.json()  
            # print(api_result2)
            
            if api_result2['state'] == "found":

                if find_method == "wNum":
        
                    api_url = API_Link + "/erp_get/wNumberChecker"
                    data = {'number_wrt': number_wrt,'brand_wrt':brand_wrt}
                    response = requests.post(api_url, data=data)

                    url_api = API_Link + "/erp_set/woupdate"

                    if response.status_code == 200:
                        api_result = response.json()  
                        if api_result['state'] == "found":
                            if api_result['register'] == "unRegisted":
                                sys_db = api_result['sys_db'] 
                                dataWRT = api_result['w_data']
                                
                                # return render(request, 'form/form_warranty.html',{'number_wrt':number_wrt,'brand_wrt':brand_wrt,'sys_db':sys_db,
                                #                                             'dataWRT':dataWRT,'dataWRT':dataWRT,'url_api':url_api})
                                return render(request, 'form/registers_warranty.html',{'number_wrt':number_wrt,'brand_wrt':brand_wrt,'sys_db':sys_db,
                                                                            'dataWRT':dataWRT,'dataWRT':dataWRT,'url_api':url_api})
                            elif api_result['register'] == "registed":
                                sys_db = api_result['sys_db']    
                                dataWRT = api_result['w_data']

                                dataWRT['cust_birthday'] = convert_date_to_thai_format(dataWRT.get('cust_birthday'))
                                dataWRT['cust_install_date'] = convert_date_to_thai_format(dataWRT.get('cust_install_date'))
                                dataWRT['cust_warrant_exdate'] = convert_date_to_thai_format(dataWRT.get('cust_warrant_exdate'))
                                # print(dataWRT)
                                
                                return render(request, 'previews/warranty_views.html',{'number_wrt':number_wrt,'brand_wrt':brand_wrt,
                                                                                       'sys_db':sys_db,'dataWRT':dataWRT })
                            else:
                                return render(request, 'errorpage/notFound.html')
                        else:
                            return render(request, 'errorpage/notFound.html') 
                    else:
                        return render(request,'form/search_warranty.html')  

                elif find_method == "cust":
                    state = api_result2['state']
                    brand = api_result2['brand']
                    w_data = api_result2['w_data']

                    return render(request, 'previews/warranty_list.html',{'state':state,'brand':brand,'w_data':w_data})
                else:
                    return render(request,'errorpage/cannotSearch.html')  
            else:
                return render(request,'errorpage/cannotSearch.html')  
        else:
            return render(request,'errorpage/cannotSearch.html')  
    else:
        return render(request,'form/search_warranty.html')  
   
    
@csrf_exempt
def showdata_wrt_list(request):

    if request.method == 'POST':
        # number_wrt = request.POST.get('number_wrt')
        # print(number_wrt)
        # return render(request, 'previews/warranty_views.html',{'number_wrt':number_wrt})
        number_wrt = request.POST.get('number_wrt')
        brand_wrt = request.POST.get('brand_wrt')

        api_url = API_Link + "/erp_get/wNumberChecker"
        data = {'number_wrt': number_wrt,'brand_wrt':brand_wrt}
        response = requests.post(api_url, data=data)

        sys_db = ""

        if response.status_code == 200:
            api_result = response.json()  
            # print(api_result)
            
            if api_result['state'] == "found":
                if api_result['register'] == "registed":
                    sys_db = api_result['sys_db']    
                    dataWRT = api_result['w_data']
                    # print(dataWRT)
                    dataWRT['cust_birthday'] = convert_date_to_thai_format(dataWRT.get('cust_birthday'))
                    dataWRT['cust_install_date'] = convert_date_to_thai_format(dataWRT.get('cust_install_date'))
                    dataWRT['cust_warrant_exdate'] = convert_date_to_thai_format(dataWRT.get('cust_warrant_exdate'))
                    return render(request, 'previews/warranty_views.html',{'number_wrt':number_wrt,'brand_wrt':brand_wrt,'sys_db':sys_db,'dataWRT':dataWRT })
                else:
                    return render(request, 'errorpage/notFound.html')
                
            elif api_result['state'] == "notFound":
                return render(request, 'errorpage/notFound.html')
            else:
                return render(request, 'errorpage/notFound.html')
        else:
            api_result = {'error': 'Cannot fetch data from API'}
            return render(request, 'errorpage/notFound.html')
    else:
        return render(request,'form/search_warranty.html')   


def registersWarranty(request):
    #หน้ากรอกหมายเลขบัตรก่อนลงทะเบียน
    
    return render(request,'form/registers_warranty.html')

@csrf_exempt
def form_warranty(request):
    if request.method == 'POST':
        number_wrt = request.POST.get('number_wrt')
        brand_wrt = request.POST.get('brand_wrt')

        api_url = API_Link + "/erp_get/wNumberChecker"
        data = {'number_wrt': number_wrt, 'brand_wrt': brand_wrt}
        response = requests.post(api_url, data=data)

        sys_db = ""
        url_api = API_Link + "/erp_set/woupdate"
        # print(url_api)
        if response.status_code == 200:
            api_result = response.json()  
            # print(api_result)
            
            if api_result['state'] == "found":
                if api_result['register'] == "unRegisted":
                    sys_db = api_result['sys_db'] 
                    dataWRT = api_result['w_data']
                    # print(dataWRT)
                    return render(request, 'form/form_warranty.html',{'number_wrt':number_wrt,'brand_wrt':brand_wrt,'sys_db':sys_db,
                                                                 'dataWRT':dataWRT,'dataWRT':dataWRT,'url_api':url_api})
                elif api_result['register'] == "registed":
                    sys_db = api_result['sys_db']    
                    dataWRT = api_result['w_data']

                    dataWRT['cust_birthday'] = convert_date_to_thai_format(dataWRT.get('cust_birthday'))
                    dataWRT['cust_install_date'] = convert_date_to_thai_format(dataWRT.get('cust_install_date'))
                    dataWRT['cust_warrant_exdate'] = convert_date_to_thai_format(dataWRT.get('cust_warrant_exdate'))
                    
                    # print(dataWRT)
                    
                    return render(request, 'previews/warranty_views.html',{'number_wrt':number_wrt,'brand_wrt':brand_wrt,'sys_db':sys_db,
                                                                  'dataWRT':dataWRT,'url_api':url_api})
                else:
                    return render(request, 'errorpage/notFound.html')
                
            elif api_result['state'] == "notFound":
                return render(request, 'errorpage/notFound.html')
            else:
                return render(request, 'errorpage/notFound.html')
        else:
            api_result = {'error': 'Cannot fetch data from API'}
            return render(request, 'errorpage/notFound.html')
    else:
        return render(request, 'form/registers_warranty.html')



@csrf_exempt
def showdata_wrt(request):

    if request.method == 'POST':
        number_wrt = request.POST.get('number_wrt')
        brand_wrt = request.POST.get('brand_wrt')

        api_url = API_Link + "/erp_get/wNumberChecker"
        data = {'number_wrt': number_wrt,'brand_wrt':brand_wrt}
        response = requests.post(api_url, data=data)

        sys_db = ""

        if response.status_code == 200:
            api_result = response.json()  
            # print(api_result)
            
            if api_result['state'] == "found":
                if api_result['register'] == "registed":
                    sys_db = api_result['sys_db']    
                    dataWRT = api_result['w_data']

                    dataWRT['cust_birthday'] = convert_date_to_thai_format(dataWRT.get('cust_birthday'))
                    dataWRT['cust_install_date'] = convert_date_to_thai_format(dataWRT.get('cust_install_date'))
                    dataWRT['cust_warrant_exdate'] = convert_date_to_thai_format(dataWRT.get('cust_warrant_exdate'))
                    # print(dataWRT)
                    
                    return render(request, 'previews/warranty_views.html',{'number_wrt':number_wrt,'brand_wrt':brand_wrt,'sys_db':sys_db,'dataWRT':dataWRT })
                else:
                    return render(request, 'errorpage/cannotSave.html')
                
            elif api_result['state'] == "notFound":
                return render(request, 'errorpage/notFound.html')
            else:
                return render(request, 'errorpage/notFound.html')
        else:
            api_result = {'error': 'Cannot fetch data from API'}
            return render(request, 'errorpage/notFound.html')
    else:
        return render(request, 'form/registers_warranty.html')



@csrf_exempt
def update_warranty(request):
    url = API_Link + "/erp_set/woupdate"
    url2 = API_Link + "/erp_set/upload-wImage/"
    
    if request.method == 'POST':
        data = {
                    'number_wrt' : request.POST.get('number_wrt'),
                    'brand_wrt' : request.POST.get('brand_wrt'),
                    'sys_db' : request.POST.get('sys_db'),
                    'product_code': request.POST.get('product_code'),
                    'cust_name' : request.POST.get('cust_name'),
                    'cust_birthday' : request.POST.get('cust_birthday'),
                    'cust_gender' : request.POST.get('cust_gender'),
                    'cust_phone' : request.POST.get('cust_phone'),
                    'cust_address' : request.POST.get('cust_address'),
                    'cust_province_id' : request.POST.get('cust_province_id'),
                    'cust_district_id' : request.POST.get('cust_district_id'),
                    'cust_subdistrict_id' : request.POST.get('cust_subdistrict_id'),
                    'cust_postalcode' : request.POST.get('cust_postalcode'),
                    'cust_carbrand_id' : request.POST.get('cust_carbrand_id'),
                    'cust_carmodel_id' : request.POST.get('cust_carmodel_id'),
                    'cust_liceseplateblack' : request.POST.get('cust_liceseplateblack'),
                    'cust_vin' : request.POST.get('cust_vin'),
                    'cust_install_date' : request.POST.get('cust_install_date'),
                    'showroominstall_id' : request.POST.get('showroominstall_id'),
                    'frontInstall_position' : request.POST.get('frontInstall_position'),
                    'frontInstall_product' : request.POST.get('frontInstall_product'),
                    'aroundInstall_position' : request.POST.get('aroundInstall_position'),
                    'aroundInstall_product' : request.POST.get('aroundInstall_product'),
                    'anotherInstall_position' : request.POST.get('anotherInstall_position'),
                    'anotherInstall_product' : request.POST.get('anotherInstall_product')
            }
        
        print(data)
        # response = requests.post(url, data=data)

        # รีีไซส์​รูปภาพก่อนจะบันทืึกรูปภาพ
        images = request.FILES.get('image')
        if images:
            if images.content_type in ['image/jpeg', 'image/png', 'image/gif', 'image/svg+xml']:
                img = Image.open(images)
                allowed_formats = ['JPEG', 'PNG', 'GIF', 'SVG']
                if img.format in allowed_formats:
                    if img.width > 1024 or img.height > 768:
                        img.thumbnail((1024, 768))
                    
                    output = io.BytesIO()
                    img.save(output, format=img.format) 
                    output.seek(0)

                    new_image = {'image': ContentFile(output.read(), name=images.name)}

                    filename = request.POST.get('filename')
                    if filename:
                        data2 = {'filename': filename}

                        response3 = requests.post(url2, data=data2, files=new_image)
                        api_result2 = response3.json()
                        # print(api_result2)
                
            else:
                return render(request, 'errorpage/errorImage.html')
            

            # บันทึกข้อมูลบัตรรับประกันหากมีรูปภาพ
            response = requests.post(url, data=data)
            # print(response)
            number_wrt = request.POST.get('number_wrt')
            brand_wrt = request.POST.get('brand_wrt') 

            if response.status_code == 200:
                
                api_result = response.json()  
                
                api_url = API_Link + "/erp_get/wNumberChecker"
                data = {'number_wrt': number_wrt, 'brand_wrt': brand_wrt}
                response2 = requests.post(api_url, data=data)

                sys_db = ""
                url_api = API_Link + "/erp_set/woupdate"
                # print(url_api)
                if response2.status_code == 200:
                    api_result = response2.json()
                    # print(api_result)
                    
                    if api_result['state'] == "found":
                        if api_result['register'] == "registed":
                            sys_db = api_result['sys_db']    
                            dataWRT = api_result['w_data']

                            dataWRT['cust_birthday'] = convert_date_to_thai_format(dataWRT.get('cust_birthday'))
                            dataWRT['cust_install_date'] = convert_date_to_thai_format(dataWRT.get('cust_install_date'))
                            dataWRT['cust_warrant_exdate'] = convert_date_to_thai_format(dataWRT.get('cust_warrant_exdate'))
                            # print(dataWRT)
                        
                            return render(request, 'previews/warranty_views.html',{'number_wrt':number_wrt,'brand_wrt':brand_wrt,'sys_db':sys_db,
                                                                        'dataWRT':dataWRT,'url_api':url_api})
                        else:
                            return render(request, 'errorpage/notFound.html')
                    else:
                        return render(request, 'errorpage/notFound.html')
                else:
                    return render(request, 'errorpage/notFound.html')
            else:
                return render(request, 'errorpage/cannotSave.html')
        else:
            return render(request, 'errorpage/errorImage.html')



@csrf_exempt
def find_provinces(request):
    url = API_Link + "/erp_get/provinceAll/"
    # print(url)
    response = urllib.request.urlopen(url)
    data = json.load(response)
    # print(data)
    return JsonResponse(data, safe=False)

@csrf_exempt
def find_districts(request):
    if request.method == 'POST':
        province_id = request.POST.get('provinceId')
        url = API_Link + "/erp_get/districtWithProvince"
        data = {'province_id': province_id}
        response = requests.post(url, data=data)
        districts = response.json()
        return JsonResponse(districts, safe=False)

    # return render(request, 'form/form_warranty.html', {'districts': districts})

@csrf_exempt
def find_subdistricts(request):
    if request.method == 'POST':
        district_id = request.POST.get('districtId')
        url = API_Link + "/erp_get/subdistrictWithDistrict"
        data = {'district_id': district_id}
        response = requests.post(url, data=data)
        
        subdistricts = response.json() 
        # print(subdistricts)
        return JsonResponse(subdistricts, safe=False)
    
@csrf_exempt
def find_zipcode(request):
    if request.method == 'POST':
        subdistrict_id = request.POST.get('SubdistrictId')
        # print(subdistrict_id)
        url = API_Link + "/erp_get/zipCodeWithDistrict"
        data = {'subdistrict_id': subdistrict_id}
        response = requests.post(url, data=data)

        zipcode = response.json()
        # print(zipcode)
        return JsonResponse(zipcode, safe=False)
    

@csrf_exempt
def find_carbrand(request):
    url = API_Link + "/erp_get/carBrand/"
    response = urllib.request.urlopen(url)
    carbrandData = json.load(response)
    return JsonResponse(carbrandData, safe=False)

@csrf_exempt
def find_carmodel(request):
    if request.method == 'POST':
        carBrand_id = request.POST.get('carbrandId')
        url = API_Link + "/erp_get/carModelWithCarModel"
        data = {'carBrand_id': carBrand_id}
        response = requests.post(url, data=data)

        carmodelData = response.json() 
        # print(carmodelData)
        return JsonResponse(carmodelData, safe=False)
    
# @csrf_exempt
# def find_gender(request):
#     # url = 'http://172.17.1.199:8003/erp_get/gender/'
#     url = API_Link + "/erp_get/gender/"
#     response = urllib.request.urlopen(url)
#     genderData = json.load(response)
#     return JsonResponse(genderData, safe=False)


@csrf_exempt
def find_provinces_contact(request):
    url = API_Link + "/erp_get/provinceAll/"
    response = urllib.request.urlopen(url)
    provinConData = json.load(response)
    return JsonResponse(provinConData, safe=False)


@csrf_exempt
def find_contact_province(request):
    if request.method == 'POST':
        province_id = request.POST.get('provinConId')
        url = API_Link + "/erp_get/cusContactWithProvice"
        data = {'province_id': province_id}
        response = requests.post(url, data=data)

        conProvinData = response.json() 
        # print(carmodelData)
        return JsonResponse(conProvinData, safe=False)

@csrf_exempt
def find_group_front(request):
    brand = "Lamina"

    url = API_Link + "/erp_get/productGroup"
    data = {'brand': brand}
    response = requests.post(url, data=data)
    GroupFrontData = response.json()  

    # print(GroupFrontData)

    return JsonResponse(GroupFrontData, safe=False)

@csrf_exempt
def find_product_front(request):
    if request.method == 'POST':
        group = request.POST.get('GroupfrontName')
        # print(group)
        url = API_Link + "/erp_get/productWithGroup"
        data = {'group': group}
        response = requests.post(url, data=data)

        ProductFrontData = response.json() 
        # print(ProductFrontData)
        return JsonResponse(ProductFrontData, safe=False)

@csrf_exempt
def find_group_around(request):
    brand = "Lamina"

    url = API_Link + "/erp_get/productGroup"
    data = {'brand': brand}
    response = requests.post(url, data=data)
    GroupAroundData = response.json()  

    # print(GroupAroundData)

    return JsonResponse(GroupAroundData, safe=False)

@csrf_exempt
def find_product_around(request):
    if request.method == 'POST':
        group = request.POST.get('GrouparoundName')
        # print(group)
        url = API_Link + "/erp_get/productWithGroup"
        data = {'group': group}
        response = requests.post(url, data=data)

        ProductFrontData = response.json() 
        # print(ProductFrontData)
        return JsonResponse(ProductFrontData, safe=False)

@csrf_exempt
def find_group_another(request):
    brand = "Lamina"

    url = API_Link + "/erp_get/productGroup"
    data = {'brand': brand}
    response = requests.post(url, data=data)
    GroupAnotherData = response.json()  

    # print(GroupAnotherData)

    return JsonResponse(GroupAnotherData, safe=False)

@csrf_exempt
def find_product_another(request):
    if request.method == 'POST':
        group = request.POST.get('GroupanotherName')
        # print(group)
        url = API_Link + "/erp_get/productWithGroup"
        data = {'group': group}
        response = requests.post(url, data=data)

        ProductFrontData = response.json() 
        # print(ProductFrontData)
        return JsonResponse(ProductFrontData, safe=False)

@csrf_exempt
def warranty_print(request):
    if request.method == "POST":
        data_text,context = showWarannty(request)
        return render(request, 'previews/print_warranty.html', context)

@csrf_exempt
def warranty_download(request):
    if request.method == "POST":
        data_text, context = downloadWarannty(request) 
        response = HttpResponse(base64.b64decode(data_text.split(",")[1]), content_type="image/jpeg")
        response['Content-Disposition'] = "attachment; filename=img.jpg"
        return response



@csrf_exempt
def notFound_page(request):
    
    return render(request, 'errorpage/notFound.html')


@csrf_exempt
def cannotSave_page(request):
    
    return render(request, 'errorpage/cannotSave.html')

@csrf_exempt
def cannotSearch_page(request):
    
    return render(request, 'errorpage/cannotSearch.html')


@csrf_exempt
def errorImage_page(request):
    
    return render(request, 'errorpage/errorImage.html')