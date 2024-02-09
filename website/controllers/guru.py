from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .. import models as db
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.core.paginator import Paginator
import json
from django.db.models import Q
import pandas as pd
from django.db import transaction


@require_GET
@login_required(login_url="/auth/login")
def views(request):
    return render(request, "guru/guru.html")


@require_GET
@login_required(login_url="/auth/login")
def get_data(request):
    page = request.GET.get("page")
    search = request.GET.get("search")
    status = request.GET.get("status")

    data = db.Guru.objects.order_by("nama")

    if search:
        data = data.filter(nama__icontains=search)

    if status:
        data = data.filter(status=status.lower() == "true")

    paginator = Paginator(data, 10)
    current_page = paginator.get_page(page)

    serialized_data = []
    for obj in current_page:
        row = {
            "id": obj.id,
            "nama": obj.nama,
            "kode": obj.kode,
            "status": obj.status,
            "foto": obj.foto.url if obj.foto else None,
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
    return render(request, "guru/add.guru.html")


@require_POST
@login_required(login_url="/auth/login")
def add_data(request):    
    nama = request.POST.get('nama')
    kode = request.POST.get('kode')
    status = str(request.POST.get('status'))
    foto = request.FILES.get('foto')

    try:
        if db.Guru.objects.filter(kode=kode).exists():
            return JsonResponse({'error': 'Guru dengan NIP/NUPTK ini sudah ada!'}, status=400)
        else:
            db.Guru.objects.create(
                nama=nama,
                kode=kode,
                status=status.lower() == "true",
                foto=foto
            )
            return JsonResponse({'success': 'Data guru berhasil disimpan'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    

@require_POST
@login_required(login_url="/auth/login")
def delete_data(request):    
    key = json.loads(request.body).get('key')

    try:
        db.Guru.objects.filter(id=key).delete()
        return JsonResponse({'success': 'Data guru berhasil dihapus'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    

@require_GET
@login_required(login_url="/auth/login")
def edit_views(request, id):
    return render(request, "guru/edit.guru.html")


@require_GET
@login_required(login_url="/auth/login")
def get_detail(request, id):
    data = db.Guru.objects.get(id=id)
    
    row = {
        "id": data.id,
        "nama": data.nama,
        "kode": data.kode,
        "status": data.status,
        "foto": data.foto.url if data.foto else None,
    }
    
    return JsonResponse(row)


@require_POST
@login_required(login_url="/auth/login")
def edit_data(request, id):    
    nama = request.POST.get('nama')
    kode = request.POST.get('kode')
    status = str(request.POST.get('status'))
    foto = request.FILES.get('foto')

    try:
        guru = db.Guru.objects.get(id=id)
        guru.nama = nama
        guru.kode = kode
        guru.status = status.lower() == "true"
        if foto:
            guru.foto = foto
        guru.save()
        return JsonResponse({'success': 'Data guru berhasil diubah'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    

@require_POST
@login_required(login_url="/auth/login")
def import_file(request):
    file = request.FILES['file']

    try:
        with transaction.atomic():
            df = pd.read_excel(file, engine='openpyxl')

            columns = df.columns

            required_columns = ['NIP/NUPTK', 'Nama']
            if not all(column in columns for column in required_columns):
                return JsonResponse({'error': 'Kolom yang diperlukan tidak ditemukan'}, status=400)

            for index, row in df.iterrows():
                if not db.Guru.objects.filter(kode=row['NIP/NUPTK']).exists():
                    try:
                        db.Guru.objects.create(
                            kode=str(row['NIP/NUPTK']),
                            nama=row['Nama'],
                        )
                    except Exception as e:
                        return JsonResponse({'error': f'Error pada baris {index + 2}: {str(e)}'}, status=400)

            return JsonResponse({'success': 'Data guru berhasil diimpor'})

    except Exception as e:
        return JsonResponse({'error': f'Error: {str(e)}'}, status=400)