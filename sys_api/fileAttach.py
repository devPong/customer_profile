

from django.db import connections
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse,HttpResponse
from datetime import datetime

cp_db = 'default'


class imgFileApi:
    @csrf_exempt
    def upload(request):
        if request.method == 'POST':
            file = request.FILES.get('imgFile')
            if file:
                file_name = file.name
                file_path = f'media/uploads/{file_name}'
                
                with open(file_path, 'wb+') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)
                
                return JsonResponse({'status': 'success', 'file_path': file_path}, status=200)
            else:
                return JsonResponse({'status': 'error', 'message': 'No file provided'}, status=400)
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
    