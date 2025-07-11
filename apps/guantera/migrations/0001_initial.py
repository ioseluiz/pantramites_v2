# Generated by Django 5.2.3 on 2025-06-25 14:45

import apps.guantera.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('gestion_flota', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CopiaPoliza',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('archivo_pdf', models.FileField(upload_to='guantera/polizas/', validators=[apps.guantera.models.validate_pdf], verbose_name='Copia PDF de la Póliza')),
                ('fecha_carga', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Carga')),
                ('poliza', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='copias_documento', to='gestion_flota.poliza')),
            ],
            options={
                'verbose_name': 'Copia de Póliza',
                'verbose_name_plural': 'Copias de Pólizas',
            },
        ),
        migrations.CreateModel(
            name='CopiaRevisadoVehicular',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('archivo_pdf', models.FileField(upload_to='guantera/revisados/', validators=[apps.guantera.models.validate_pdf], verbose_name='Copia PDF del Revisado')),
                ('fecha_carga', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Carga')),
                ('revisado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='copias_documento', to='gestion_flota.revisadovehicular')),
            ],
            options={
                'verbose_name': 'Copia de Revisado Vehicular',
                'verbose_name_plural': 'Copias de Revisados Vehiculares',
            },
        ),
        migrations.CreateModel(
            name='CopiaTarjetaPesosDimensiones',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('archivo_pdf', models.FileField(upload_to='guantera/pesos_dimensiones/', validators=[apps.guantera.models.validate_pdf], verbose_name='Copia PDF de la Tarjeta')),
                ('fecha_carga', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Carga')),
                ('tarjeta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='copias_documento', to='gestion_flota.tarjetapesosdimensiones')),
            ],
            options={
                'verbose_name': 'Copia de Tarjeta de Pesos y Dimensiones',
                'verbose_name_plural': 'Copias de Tarjetas de Pesos y Dimensiones',
            },
        ),
        migrations.CreateModel(
            name='FotoVehiculo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('foto', models.ImageField(upload_to='guantera/fotos/', verbose_name='Archivo Foto')),
                ('descripcion', models.CharField(blank=True, max_length=255, verbose_name='Descripcion')),
                ('fecha_carga', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Carga')),
                ('vehiculo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fotos', to='gestion_flota.vehiculo')),
            ],
            options={
                'verbose_name': 'Foto de Vehículo',
                'verbose_name_plural': 'Fotos de Vehículos',
                'ordering': ['-fecha_carga'],
            },
        ),
        migrations.CreateModel(
            name='ReciboPagoPlaca',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('periodo', models.CharField(max_length=20, verbose_name='Periodo de Pago (e.g., 2025)')),
                ('fecha_pago', models.DateField(verbose_name='Fecha de Pago')),
                ('monto', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Monto Pagado')),
                ('archivo_pdf', models.FileField(upload_to='guantera/recibos_placa/', validators=[apps.guantera.models.validate_pdf], verbose_name='Copia PDF del Recibo')),
                ('fecha_carga', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Carga')),
                ('vehiculo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recibos_placa', to='gestion_flota.vehiculo')),
            ],
            options={
                'verbose_name': 'Recibo de Pago de Placa',
                'verbose_name_plural': 'Recibos de Pago de Placa',
                'ordering': ['-fecha_pago'],
            },
        ),
        migrations.CreateModel(
            name='RegistroUnicoVehicular',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('archivo_pdf', models.FileField(upload_to='guantera/registros/', validators=[apps.guantera.models.validate_pdf], verbose_name='Archivo PDF del Registro')),
                ('fecha_emision', models.DateField(verbose_name='Fecha de Emisión del Documento')),
                ('fecha_carga', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Carga')),
                ('vehiculo', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='registro_unico', to='gestion_flota.vehiculo')),
            ],
            options={
                'verbose_name': 'Registro Único Vehicular',
                'verbose_name_plural': 'Registros Únicos Vehiculares',
            },
        ),
        migrations.CreateModel(
            name='StickerPlaca',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('año', models.PositiveIntegerField(verbose_name='Año del Sticker')),
                ('archivo_pdf', models.FileField(upload_to='guantera/stickers_placa/', validators=[apps.guantera.models.validate_pdf], verbose_name='Copia PDF del Sticker')),
                ('fecha_carga', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Carga')),
                ('vehiculo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stickers_placa', to='gestion_flota.vehiculo')),
            ],
            options={
                'verbose_name': 'Sticker de Placa',
                'verbose_name_plural': 'Stickers de Placa',
                'ordering': ['-año'],
                'unique_together': {('vehiculo', 'año')},
            },
        ),
    ]
