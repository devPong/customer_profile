from django.db import connections
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse,HttpResponse
from datetime import datetime

cp_db = 'default'

def conn_fetchall(dataBase,q_txt):
    rawDatas = None
    with connections[dataBase].cursor() as cursor:
        cursor.execute(q_txt)
        rawDatas = cursor.fetchall()
    return rawDatas

class addressApi:
    @csrf_exempt
    def province_all (request):
        q_txt = 'select p.id,p."name" from province p order by p."name";'
        rawDatas = conn_fetchall(cp_db,q_txt)
        return JsonResponse(rawDatas , json_dumps_params={'ensure_ascii': False} ,safe=False)

    @csrf_exempt
    def district_withProvince (request):
        if  request.method == 'POST':
            province_id = request.POST.get('province_id')
            q_txt = 'select d.id,d."name" from district d where d.province_id  = %s order by d."name";' %(province_id)
            rawDatas = conn_fetchall(cp_db,q_txt)
            return JsonResponse(rawDatas , json_dumps_params={'ensure_ascii': False} ,safe=False)
        else:
            return JsonResponse(True ,safe=False)

    @csrf_exempt
    def subdistrict_withDistrict (request):
        if  request.method == 'POST':
            district_id = request.POST.get('district_id')
            q_txt = f'select s.id,s."name",s.code from subdistrict s where s.district_id = %s order by s."name" ;' %(district_id)
            rawDatas = conn_fetchall(cp_db,q_txt)
            return JsonResponse(rawDatas , json_dumps_params={'ensure_ascii': False} ,safe=False)
        else:
            return JsonResponse(True ,safe=False)
        
    # @csrf_exempt
    # def zipCode_withSubdistrict (request):
    #     if  request.method == 'POST':
    #         subdistrict_id = request.POST.get('subdistrict_id')
    #         q_txt = f'select s.id,s."name" from subdistrict s where s.district_id = %s order by s."name" ;' %(district_id)
    #         datas = sorted(datas, key=lambda x: x['code'])
    #         return JsonResponse(datas , json_dumps_params={'ensure_ascii': False} ,safe=False)
    #     else:
    #         return JsonResponse(True ,safe=False)
        