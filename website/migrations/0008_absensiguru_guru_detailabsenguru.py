# Generated by Django 5.0.1 on 2024-02-07 13:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0007_siswa_foto'),
    ]

    operations = [
        migrations.CreateModel(
            name='AbsensiGuru',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tanggal', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Guru',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kode', models.CharField(max_length=100)),
                ('nama', models.CharField(max_length=255)),
                ('status', models.BooleanField(default=True)),
                ('foto', models.ImageField(null=True, upload_to='foto/')),
            ],
        ),
        migrations.CreateModel(
            name='DetailAbsenGuru',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jam_masuk', models.TimeField()),
                ('jam_keluar', models.TimeField()),
                ('absensi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detail', to='website.absensiguru')),
                ('guru', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='guru', to='website.guru')),
            ],
        ),
    ]
