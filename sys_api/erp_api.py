from django.db import connections
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse,HttpResponse
from datetime import datetime

erpDB = 'erp_db'

def conn_fetchall(dataBase,q_txt):
    rawDatas = None
    with connections[dataBase].cursor() as cursor:
        cursor.execute(q_txt)
        rawDatas = cursor.fetchall()
    return rawDatas

class contactERP:
    @csrf_exempt
    def contact_all (request):
        q_txt = 'select c.id, c.code, c."name", c.branch from contact c ;'
        rawDatas = conn_fetchall(erpDB,q_txt)
        return JsonResponse(rawDatas , json_dumps_params={'ensure_ascii': False} ,safe=False)
