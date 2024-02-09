from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .. import models as db
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_GET, require_POST
from django.core.paginator import Paginator
import json, locale
import pandas as pd
from django.utils import formats
from datetime import datetime
from django.db.models.functions import ExtractYear, ExtractMonth
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.styles import Border, Side
from calendar import month_name


locale.setlocale(locale.LC_TIME, 'id_ID.UTF-8')


@require_GET
@login_required(login_url="/auth/login")
def views(request):
    kelas = db.Kelas.objects.order_by('angka')
    tahun_absensi = db.Absensi.objects.annotate(tahun=ExtractYear('tanggal'))
    tahun_unik = tahun_absensi.values_list('tahun', flat=True).distinct()

    bulan_absensi = db.Absensi.objects.annotate(bulan=ExtractMonth('tanggal'))
    bulan_unik = bulan_absensi.values_list('bulan', flat=True).distinct()

    nama_bulan = month_name[1:]

    select_options = [(bulan, nama_bulan[bulan-1]) for bulan in bulan_unik]

    return render(request, "absensi/absensi.html", {
        'kelas': kelas,
        'tahun': tahun_unik,
        'bulan': select_options
    })


@require_GET
@login_required(login_url="/auth/login")
def get_data(request):
    page = request.GET.get("page")
    date = request.GET.get("date")
    filter = request.GET.get("filter")
    year = request.GET.get("year")

    data = db.Absensi.objects.order_by("-id")

    if date:
        data = data.filter(tanggal__month=date)

    if filter:
        data = data.filter(kelas__id=filter)

    if year:
        data = data.filter(tanggal__year=year)

    paginator = Paginator(data, 10)
    current_page = paginator.get_page(page)

    serialized_data = []
    for obj in current_page:
        row = {
            "id": obj.id,
            "kelas": f"{obj.kelas.angka} {obj.kelas.rombel}",
            "tanggal": formats.date_format(obj.tanggal, format='l, d M Y'),
            "absensi": {
                "hadir": obj.detail.all().count(),
                "absen": db.Kelas.objects.get(id=obj.kelas.id).siswa.filter(status=True).count() - obj.detail.all().count()
            },
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
    

@require_POST
@login_required(login_url="/auth/login")
def delete_data(request):    
    key = json.loads(request.body).get('key')

    try:
        db.Absensi.objects.filter(id=key).delete()
        return JsonResponse({'success': 'Absensi berhasil dihapus'})
    except:
        return JsonResponse({'error': "Absensi gagal dihapus!"}, status=400)
    

@require_GET
@login_required(login_url="/auth/login")
def detail_views(request, id):
    kelas = db.Kelas.objects.order_by('angka')
    return render(request, "absensi/detail.absensi.html", {'kelas': kelas})


@require_GET
@login_required(login_url="/auth/login")
def get_detail(request, id):
    data = db.Absensi.objects.get(id=id)

    detail = []
    for d in db.DetailAbsen.objects.filter(absensi=data).order_by('siswa'):
        detail.append({
            'nama': d.siswa.nama_lengkap,
            'nisn': d.siswa.nisn,
            'foto': d.siswa.foto.url if d.siswa.foto else None
        })
    
    row = {
        "id": data.id,
        "kelas": f"{data.kelas.angka} {data.kelas.rombel}" ,
        "tanggal": formats.date_format(data.tanggal, format='l, d M Y'),
        "detail": detail,
    }
    
    return JsonResponse(row)


@require_GET
@login_required(login_url="/auth/login")
def download(request):
    bulan = request.GET.get('month')
    kelas = request.GET.get('kelas')
    tahun = request.GET.get('year')

    # Ambil data kelas
    kelas = get_object_or_404(db.Kelas, id=kelas)
    
    # Ambil data absensi sesuai bulan
    absensi = db.Absensi.objects.filter(kelas=kelas, tanggal__month=bulan, tanggal__year=tahun)
    
    # Ambil semua siswa di kelas ini
    siswa_kelas = kelas.siswa.all()
    
    # Buat dataframe kosong untuk menyimpan data absensi
    columns = ['No.', 'NISN', 'Nama', 'Kelas'] + [str(date) for date in absensi.values_list('tanggal', flat=True)]
    df = pd.DataFrame(columns=columns)
    
    # Isi dataframe dengan data absensi
    for i, siswa in enumerate(siswa_kelas, start=1):
        row_data = [i, siswa.nisn, siswa.nama_lengkap, f"{kelas.angka}{kelas.rombel}"]
        for tanggal in absensi.values_list('tanggal', flat=True):
            detail_absen = db.DetailAbsen.objects.filter(siswa__id=siswa.id, absensi__kelas=kelas, absensi__tanggal=tanggal).first()
            if detail_absen:
                row_data.append('M')
            else:
                row_data.append('-')
        df.loc[len(df)] = row_data
    
    # Buat nama file
    nama_file = f"Data Absen - Kelas {kelas.angka}{kelas.rombel} - {datetime.strptime(str(bulan), '%m').strftime('%B')} {tahun}.xlsx"

    # Inisialisasi workbook
    wb = Workbook()
    ws = wb.active
    
    # Menambahkan judul
    ws.title = "Data Absensi"
    ws.append(["DATA ABSENSI SDN 1 AJI JAYA"])
    ws.append(["Kelas", f"{kelas.angka}{kelas.rombel}"])
    ws.append(["Bulan", datetime.strptime(str(bulan), '%m').strftime('%B')])
    ws.append(["Tahun", tahun])
    ws.append([])  # Baris kosong
    
    # Menambahkan data absensi
    for r in dataframe_to_rows(df, index=False, header=True):
        ws.append(r)

    # Menambahkan border pada tabel
    thin_border = Border(left=Side(style='thin'), 
                         right=Side(style='thin'), 
                         top=Side(style='thin'), 
                         bottom=Side(style='thin'))
    for row in ws.iter_rows(min_row=6, max_row=6+len(df), min_col=1, max_col=len(columns)):
        for cell in row:
            cell.border = thin_border
    
    # Buat response Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{nama_file}"'
    
    wb.save(response)
    
    return response