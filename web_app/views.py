from django.shortcuts import render

# Create your views here.


def contact_management(request):

    return render(request, 'web_app/admin_contact_edit.html')