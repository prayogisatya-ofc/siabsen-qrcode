from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_delete, pre_save
from PIL import Image
import io
import uuid

class Kelas(models.Model):
    romawi = models.CharField(max_length=5)
    angka = models.IntegerField()
    rombel = models.CharField(max_length=1)

    def __str__(self):
        return f"{self.angka} {self.rombel}"
    

class Siswa(models.Model):
    nisn = models.CharField(max_length=50)
    nama_lengkap = models.CharField(max_length=255)
    kelas = models.ForeignKey(Kelas, on_delete=models.CASCADE, related_name='siswa')
    status = models.BooleanField(default=True, null=True)
    foto = models.ImageField(upload_to='foto/', null=True)

    def __str__(self):
        return self.nama_lengkap
    
    def save(self, *args, **kwargs):
        if self.foto:
            if self.id:
                orig_image = Siswa.objects.get(id=self.id).foto
                if orig_image != self.foto:
                    self.compress_image()
            else:
                self.compress_image()
        super(Siswa, self).save(*args, **kwargs)

    def compress_image(self):
        img = Image.open(self.foto)
        max_size = (400, 400)
        img.thumbnail(max_size, Image.LANCZOS)
        temp_image = io.BytesIO()
        img.save(temp_image, 'JPEG', quality=70)
        self.foto.delete(save=False)
        self.foto.save(f"{uuid.uuid4().hex[:15]}.jpg", temp_image, save=False)
    
@receiver(post_delete, sender=Siswa)
def delete_foto_siswa(sender, **kwargs):
    ins = kwargs['instance']
    try:
        ins.foto.delete(save=False)
    except:
        pass

@receiver(pre_save, sender=Siswa)
def update_foto_siswa(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_file = Siswa.objects.get(pk=instance.pk).foto
        except Siswa.DoesNotExist:
            return False
        else:
            new_file = instance.foto
            if old_file and old_file.url != new_file.url:
                old_file.delete(save=False) 
    

class Absensi(models.Model):
    kelas = models.ForeignKey(Kelas, on_delete=models.CASCADE)
    tanggal = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.kelas.romawi} {self.kelas.rombel} - {self.tanggal}"
    

class DetailAbsen(models.Model):
    absensi = models.ForeignKey(Absensi, on_delete=models.CASCADE, related_name='detail')
    siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE, related_name='siswa')


class Guru(models.Model):
    kode = models.CharField(max_length=100)
    nama = models.CharField(max_length=255)
    status = models.BooleanField(default=True)
    foto = models.ImageField(upload_to='foto/', null=True)

    def __str__(self):
        return self.nama
    
    def save(self, *args, **kwargs):
        if self.foto:
            if self.id:
                orig_image = Guru.objects.get(id=self.id).foto
                if orig_image != self.foto:
                    self.compress_image()
            else:
                self.compress_image()
        super(Guru, self).save(*args, **kwargs)

    def compress_image(self):
        img = Image.open(self.foto)
        max_size = (400, 400)
        img.thumbnail(max_size, Image.LANCZOS)
        temp_image = io.BytesIO()
        img.save(temp_image, 'JPEG', quality=70)
        self.foto.delete(save=False)
        self.foto.save(f"{uuid.uuid4().hex[:15]}.jpg", temp_image, save=False)
    
@receiver(post_delete, sender=Guru)
def delete_foto_guru(sender, **kwargs):
    ins = kwargs['instance']
    try:
        ins.foto.delete(save=False)
    except:
        pass

@receiver(pre_save, sender=Guru)
def update_foto_guru(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_file = Guru.objects.get(pk=instance.pk).foto
        except Guru.DoesNotExist:
            return False
        else:
            new_file = instance.foto
            if old_file and old_file.url != new_file.url:
                old_file.delete(save=False) 


class AbsensiGuru(models.Model):
    tanggal = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Absen Guru - {self.tanggal}"
    

class DetailAbsenGuru(models.Model):
    absensi = models.ForeignKey(AbsensiGuru, on_delete=models.CASCADE, related_name='detail')
    guru = models.ForeignKey(Guru, on_delete=models.CASCADE, related_name='guru')
    jam_masuk = models.TimeField(auto_now_add=False, null=True)
    jam_keluar = models.TimeField(auto_now_add=False, null=True)