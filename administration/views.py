from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
# Create your views here.

@user_passes_test(lambda u:u.is_staff, login_url='login',)
def adminStore(request):

    return render(request, 'administration/administracion.html')