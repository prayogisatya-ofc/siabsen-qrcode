from django.shortcuts import render, redirect
from .. import models as db
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import check_password
import json
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required


@require_GET
def views(request):
    # if request.user.is_authenticated:
    #     return redirect('admin_dashboard_view')
    # else:
    return render(request, "login.html")


@require_POST
def auth(request):
    data = json.loads(request.body)
    
    username = data.get("username")
    password = data.get("password")
    
    user = User.objects.filter(username=username)
    if user.exists():
        cek_pass = check_password(password, user[0].password)
        if cek_pass:
            login(request, user[0])
            return JsonResponse({'success': 'Autentikasi berhasil'})

    return JsonResponse({'error': 'Username atau Password ada yang salah!'}, status=403)
    

@require_GET
@login_required(login_url='/auth/login')
def logouts(request):
    logout(request)
    return redirect("login_views")