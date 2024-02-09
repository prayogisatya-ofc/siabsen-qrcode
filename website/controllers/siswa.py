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
    kelas = db.Kelas.objects.order_by('angka')
    return render(request, "siswa/siswa.html", {'kelas': kelas})


@require_GET
@login_required(login_url="/auth/login")
def get_data(request):
    page = request.GET.get("page")
    search = request.GET.get("search")
    filter = request.GET.get("filter")
    status = request.GET.get("status")

    data = db.Siswa.objects.order_by("nama_lengkap")

    if search:
        data = data.filter(nama_lengkap__icontains=search)

    if filter:
        data = data.filter(kelas__id=filter)

    if status:
        data = data.filter(status=status.lower() == "true")

    paginator = Paginator(data, 10)
    current_page = paginator.get_page(page)

    serialized_data = []
    for obj in current_page:
        row = {
            "id": obj.id,
            "nama": obj.nama_lengkap,
            "nisn": obj.nisn,
            "kelas": f"{obj.kelas.angka} {obj.kelas.rombel}",
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
    kelas = db.Kelas.objects.order_by('angka')
    return render(request, "siswa/add.siswa.html", {'kelas': kelas})


@require_POST
@login_required(login_url="/auth/login")
def add_data(request):    
    nama = request.POST.get('nama')
    nisn = request.POST.get('nisn')
    kelas = request.POST.get('kelas')
    status = str(request.POST.get('status'))
    foto = request.FILES.get('foto')

    try:
        if db.Siswa.objects.filter(nisn=nisn).exists():
            return JsonResponse({'error': 'Siswa dengan NISN ini sudah ada!'}, status=400)
        else:
            db.Siswa.objects.create(
                nama_lengkap=nama,
                nisn=nisn,
                kelas=db.Kelas.objects.get(id=kelas),
                status=status.lower() == "true",
                foto=foto
            )
            return JsonResponse({'success': 'Data siswa berhasil disimpan'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    

@require_POST
@login_required(login_url="/auth/login")
def delete_data(request):    
    key = json.loads(request.body).get('key')

    try:
        db.Siswa.objects.filter(id=key).delete()
        return JsonResponse({'success': 'Data siswa berhasil dihapus'})
    except:
        return JsonResponse({'error': "Data siswa gagal dihapus!"}, status=400)
    

@require_GET
@login_required(login_url="/auth/login")
def edit_views(request, id):
    kelas = db.Kelas.objects.order_by('angka')
    return render(request, "siswa/edit.siswa.html", {'kelas': kelas})


@require_GET
@login_required(login_url="/auth/login")
def get_detail(request, id):
    data = db.Siswa.objects.get(id=id)
    
    row = {
        "id": data.id,
        "nama": data.nama_lengkap,
        "nisn": data.nisn,
        "kelas": data.kelas.id,
        "status": data.status,
        "foto": data.foto.url if data.foto else None,
    }
    
    return JsonResponse(row)


@require_POST
@login_required(login_url="/auth/login")
def edit_data(request, id):    
    nama = request.POST.get('nama')
    nisn = request.POST.get('nisn')
    kelas = request.POST.get('kelas')
    status = str(request.POST.get('status'))
    foto = request.FILES.get('foto')

    try:
        siswa = db.Siswa.objects.get(id=id)
        siswa.nama_lengkap = nama
        siswa.nisn = nisn
        siswa.kelas = db.Kelas.objects.get(id=kelas)
        siswa.status = status.lower() == "true"
        if foto:
            siswa.foto = foto
        siswa.save()
        return JsonResponse({'success': 'Data siswa berhasil diubah'})
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

            required_columns = ['NISN', 'Nama', 'Kode Kelas']
            if not all(column in columns for column in required_columns):
                return JsonResponse({'error': 'Kolom yang diperlukan tidak ditemukan'}, status=400)

            for index, row in df.iterrows():
                if not db.Siswa.objects.filter(nisn=row['NISN']).exists():
                    try:
                        db.Siswa.objects.create(
                            nisn=row['NISN'],
                            nama_lengkap=row['Nama'],
                            kelas=db.Kelas.objects.get(romawi=row['Kode Kelas'])
                        )
                    except Exception as e:
                        return JsonResponse({'error': f'Error pada baris {index + 2}: {str(e)}'}, status=400)

            return JsonResponse({'success': 'Data siswa berhasil diimpor'})

    except Exception as e:
        return JsonResponse({'error': f'Error: {str(e)}'}, status=400)