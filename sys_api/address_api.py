
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse,HttpResponse
from datetime import datetime
from .db_engine import get_sqlalchemy_engine
import pandas as pd


cp_db = 'default'

class addressApi:
    @csrf_exempt
    def province_all (request):
        q_txt = 'select p.id,p."name" from province p order by p."name";'
        dbEngine = get_sqlalchemy_engine()
        df = pd.read_sql_query(q_txt, dbEngine)
        rawDatas = df.to_dict(orient='records')
        return JsonResponse(rawDatas , json_dumps_params={'ensure_ascii': False} ,safe=False)

    @csrf_exempt
    def district_withProvince (request):
        province_id = request.GET.get('province_id')
        q_txt = 'select d.id,d."name" from district d where d.province_id  = %s order by d."name";' %(province_id)
        dbEngine = get_sqlalchemy_engine()
        df = pd.read_sql_query(q_txt, dbEngine)
        rawDatas = df.to_dict(orient='records')
        return JsonResponse(rawDatas , json_dumps_params={'ensure_ascii': False} ,safe=False)
    

    @csrf_exempt
    def subdistrict_withDistrict (request):
        district_id = request.GET.get('district_id')
        q_txt = f'select s.id,s."name",s.code from subdistrict s where s.district_id = %s order by s."name" ;' %(district_id)
        dbEngine = get_sqlalchemy_engine()
        df = pd.read_sql_query(q_txt, dbEngine)
        rawDatas = df.to_dict(orient='records')
        return JsonResponse(rawDatas , json_dumps_params={'ensure_ascii': False} ,safe=False)
       
        
