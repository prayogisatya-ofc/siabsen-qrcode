from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .. import models as db
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.core.paginator import Paginator
import json, datetime, asyncio
from .telegrambot import send_telegram_message


@require_GET
@login_required(login_url="/auth/login")
def views(request):
    return render(request, "scanqr.html")


@require_POST
@login_required(login_url="/auth/login")
def absensi(request):    
    data = json.loads(request.body)
    kode = data.get('kode')
    type = data.get('type')

    try:
        if type == 'siswa':
            siswa = db.Siswa.objects.get(nisn=kode)
            kelas = db.Kelas.objects.get(id=siswa.kelas.id)
            tanggal_hari_ini = datetime.date.today()

            absensi_hari_ini, created = db.Absensi.objects.get_or_create(
                tanggal=tanggal_hari_ini,
                kelas=kelas
            )
            
            if db.DetailAbsen.objects.filter(siswa=siswa, absensi=absensi_hari_ini).exists():
                return JsonResponse({'error': 'Siswa sudah melakukan absen hari ini!'}, status=400)
            
            if siswa.status == False:
                return JsonResponse({'error': 'Siswa sudah lulus atau alumni!'}, status=400)
            
            detail = db.DetailAbsen.objects.create(
                absensi=absensi_hari_ini, 
                siswa=db.Siswa.objects.get(nisn=kode)
            )
            return JsonResponse({
                'success': f"<b>{detail.siswa.nama_lengkap}</b> kelas <b>{kelas.angka} {kelas.rombel}</b>",
                'foto': detail.siswa.foto.url if detail.siswa.foto else None
            })
        
        elif type == 'guru':
            guru = db.Guru.objects.get(kode=kode)
            tanggal_hari_ini = datetime.date.today()
            
            absensi_guru_hari_ini, created = db.AbsensiGuru.objects.get_or_create(
                tanggal=tanggal_hari_ini
            )

            if db.DetailAbsenGuru.objects.filter(guru=guru, absensi=absensi_guru_hari_ini, jam_masuk__isnull=False, jam_keluar__isnull=False).exists():
                return JsonResponse({'error': 'Guru sudah melakukan absen hari ini!'}, status=400)

            if not db.DetailAbsenGuru.objects.filter(absensi=absensi_guru_hari_ini, guru=guru).exists():
                jam_masuk = datetime.datetime.now().time().strftime('%H:%M:%S')
                db.DetailAbsenGuru.objects.create(
                    absensi=absensi_guru_hari_ini,
                    guru=guru,
                    jam_masuk=jam_masuk
                )
                asyncio.run(send_telegram_message(f"{guru.nama} melakukan absen masuk pada jam {jam_masuk} WIB"))
                return JsonResponse({
                    'success': f"<b>{guru.nama}</b> berhasil melakukan absen <b>masuk</b>.",
                    'foto': guru.foto.url if guru.foto else None
                })
            else:
                detail_absensi_guru = db.DetailAbsenGuru.objects.get(guru=guru, absensi=absensi_guru_hari_ini)
                jam_keluar = datetime.datetime.now().time().strftime('%H:%M:%S')
                detail_absensi_guru.jam_keluar = jam_keluar
                detail_absensi_guru.save()
                asyncio.run(send_telegram_message(f"{guru.nama} melakukan absen keluar pada jam {jam_keluar} WIB"))
                return JsonResponse({
                    'success': f"<b>{guru.nama}</b> berhasil melakukan absen <b>keluar</b>.",
                    'foto': guru.foto.url if guru.foto else None
                })
    
    except db.Siswa.DoesNotExist:
        return JsonResponse({'error': "Siswa tidak ditemukan!"}, status=400)
    except db.Guru.DoesNotExist:
        return JsonResponse({'error': "Guru tidak ditemukan!"}, status=400)
    except db.Kelas.DoesNotExist:
        return JsonResponse({'error': "Kelas tidak ditemukan!"}, status=400)