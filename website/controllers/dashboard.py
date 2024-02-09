from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .. import models as db
from django.http import JsonResponse
from django.utils.timezone import now, timedelta
from django.views.decorators.http import require_GET, require_POST


@require_GET
@login_required(login_url="/auth/login")
def views(request):
    siswa = db.Siswa.objects.all()
    kelas = db.Kelas.objects.all()
    absen = db.Absensi.objects

    start_of_week = now().date() - timedelta(days=now().weekday())
    end_of_week = start_of_week + timedelta(days=6)

    context = {
        'total_siswa': siswa.count(),
        'total_kelas': kelas.count(),
        'absen_hari_ini': absen.filter(tanggal=now().date()).count(),
        'absen_minggu_ini': absen.filter(tanggal__range=[start_of_week, end_of_week]).count()
    }
    return render(request, "dashboard.html", context)


@require_GET
@login_required(login_url="/auth/login")
def get_today(request):
    data = db.Absensi.objects.filter(tanggal=now().date())

    labels = []
    series = []
    for absen in data:
        labels.append(f"{absen.kelas.angka} {absen.kelas.rombel}")
        series.append(round(absen.detail.count() / absen.kelas.siswa.count() * 100))
    
    return JsonResponse({
        'labels': labels,
        'series': series
    })


@require_GET
@login_required(login_url="/auth/login")
def get_today_guru(request):
    data = db.AbsensiGuru.objects.filter(tanggal=now().date())

    series = []
    for absen in data:
        series.append(round(absen.detail.count() / db.Guru.objects.count() * 100))
    
    return JsonResponse({'series': series})