from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse,HttpResponse
from datetime import datetime
from .db_engine import get_sqlalchemy_engine
import pandas as pd


class personApi:
    def person_mangement(request):
        if request.method == 'POST':
            if request.POST.get.action == 'create':
                pass
            elif  request.POST.get.action == 'edit':
                pass
            elif  request.POST.get.action == 'active':
                if  request.POST.get.state == 'active':
                    pass
                elif request.POST.get.state == 'disactive':
                    pass
                else: 
                    pass
            else:
                pass
        else:
            pass
    def person_edit():
        pass