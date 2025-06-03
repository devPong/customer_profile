
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse,HttpResponse
from datetime import datetime
from db_engine import get_sqlalchemy_engine
import pandas as pd


cp_db = 'default'

# def conn_fetchall(dataBase,q_txt):
#     rawDatas = None
#     with connections[dataBase].cursor() as cursor:
#         cursor.execute(q_txt)
#         rawDatas = cursor.fetchall()
#     return rawDatas

# def pd_conn(dataBase, q_txt):
#     conn = connections[dataBase]
#     df = pd.read_sql_query(q_txt, conn)
#     return df.to_dict(orient='records')

# def get_sqlalchemy_engine(db_key='default'):
#     db = settings.DATABASES[db_key]
#     password = quote_plus(db['PASSWORD']) 
#     db_url = f"postgresql://{db['USER']}:{password}@{db['HOST']}:{db['PORT']}/{db['NAME']}"
#     return create_engine(db_url)


class addressApi:
    @csrf_exempt
    def province_all (request):
        q_txt = 'select p.id,p."name" from province p order by p."name";'
        # rawDatas = conn_fetchall(cp_db,q_txt)
        dbEngine = get_sqlalchemy_engine()
        df = pd.read_sql_query(q_txt, dbEngine)
        rawDatas = df.to_dict(orient='records')
        # rawDatas = pd_conn(cp_db,q_txt)
        
        return JsonResponse(rawDatas , json_dumps_params={'ensure_ascii': False} ,safe=False)

    @csrf_exempt
    def district_withProvince (request):
        province_id = request.GET.get('province_id')
        q_txt = 'select d.id,d."name" from district d where d.province_id  = %s order by d."name";' %(province_id)
        # rawDatas = conn_fetchall(cp_db,q_txt)
        dbEngine = get_sqlalchemy_engine()
        df = pd.read_sql_query(q_txt, dbEngine)
        rawDatas = df.to_dict(orient='records')
        return JsonResponse(rawDatas , json_dumps_params={'ensure_ascii': False} ,safe=False)
    

    @csrf_exempt
    def subdistrict_withDistrict (request):
        district_id = request.GET.get('district_id')
        q_txt = f'select s.id,s."name",s.code from subdistrict s where s.district_id = %s order by s."name" ;' %(district_id)
        # rawDatas = conn_fetchall(cp_db,q_txt)
        dbEngine = get_sqlalchemy_engine()
        df = pd.read_sql_query(q_txt, dbEngine)
        rawDatas = df.to_dict(orient='records')
        return JsonResponse(rawDatas , json_dumps_params={'ensure_ascii': False} ,safe=False)
       
        
    # @csrf_exempt
    # def zipCode_withSubdistrict (request):
    #     if  request.method == 'POST':
    #         subdistrict_id = request.POST.get('subdistrict_id')
    #         q_txt = f'select s.id,s."name" from subdistrict s where s.district_id = %s order by s."name" ;' %(district_id)
    #         datas = sorted(datas, key=lambda x: x['code'])
    #         return JsonResponse(datas , json_dumps_params={'ensure_ascii': False} ,safe=False)
    #     else:
    #         return JsonResponse(True ,safe=False)
        