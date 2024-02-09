from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .. import models as db
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.core.paginator import Paginator
import json
from django.db.models import Q

@require_GET
@login_required(login_url="/auth/login")
def views(request):
    return render(request, "kelas/kelas.html")


@require_GET
@login_required(login_url="/auth/login")
def get_data(request):
    page = request.GET.get("page")
    search = request.GET.get("search")

    data = db.Kelas.objects.order_by("angka")

    if search:
        data = data.filter(
            Q(romawi__icontains=search) |
            Q(angka__icontains=search) |
            Q(rombel__icontains=search)
        )

    paginator = Paginator(data, 10)
    current_page = paginator.get_page(page)

    serialized_data = []
    for obj in current_page:
        row = {
            "id": obj.id,
            "angka": obj.angka,
            "rombel": obj.rombel,
            "romawi": obj.romawi,
            "siswa": obj.siswa.filter(status=True).count()
        }
        serialized_data.append(row)
            
    pagination_info = {
        'has_next': current_page.has_next(),
        'has_previous': current_page.has_previous(),
        'current_page_number': current_page.number,
        'total_page': paginator.num_pages,
        'total_data': data.count()
    }
    
    response_data = {
        'data': serialized_data,
        'pagination': pagination_info
    }
        
    return JsonResponse(json.dumps(response_data), safe=False)


@require_GET
@login_required(login_url="/auth/login")
def add_views(request):
    return render(request, "kelas/add.kelas.html")


@require_POST
@login_required(login_url="/auth/login")
def add_data(request):    
    datas = json.loads(request.body)

    try:
        for data in datas:
            if data.get('angka') != '' and data.get('rombel') != '' and data.get('romawi') != '':
                db.Kelas.objects.create(angka=data.get('angka'), rombel=data.get('rombel'), romawi=data.get('romawi'))
        return JsonResponse({'success': 'Data kelas berhasil disimpan'})
    except:
        return JsonResponse({'error': "Data kelas gagal disimpan!"}, status=400)


@require_POST
@login_required(login_url="/auth/login")
def delete_data(request):    
    key = json.loads(request.body).get('key')

    try:
        db.Kelas.objects.filter(id=key).delete()
        return JsonResponse({'success': 'Data kelas berhasil dihapus'})
    except:
        return JsonResponse({'error': "Data kelas gagal dihapus!"}, status=400)
    

@require_POST
@login_required(login_url="/auth/login")
def edit_data(request):
    data = json.loads(request.body)
    id = data.get('id')
    angka = data.get('angka')
    rombel = data.get('rombel')
    romawi = data.get('romawi')

    try:
        data = db.Kelas.objects.get(id=id)
        data.angka = angka
        data.rombel = rombel
        data.romawi = romawi
        data.save()
        
        return JsonResponse({'success': 'Data kelas berhasil diupdate'})
    except:
        return JsonResponse({'error': "Data kelas gagal diupdate!"}, status=400)
    

@require_POST
@login_required(login_url="/auth/login")
def upgrade(request):
    id = json.loads(request.body).get('key')

    try:
        data = db.Kelas.objects.get(id=id)
        if data.siswa.filter(status=True).count() == 0:
            return JsonResponse({'error': 'Tidak ada siswa dalam kelas ini'}, status=400)
        
        if data.angka == 6:
            data.siswa.all().update(status=False)
        else:
            kelas_now = db.Kelas.objects.get(angka=data.angka + 1, rombel=data.rombel)
            data.siswa.all().update(
                kelas=kelas_now
            )
        
        return JsonResponse({'success': 'Siswa dinaikan kelas'})
    except:
        return JsonResponse({'error': "Siswa gagal dinaikan kelas!"}, status=400)