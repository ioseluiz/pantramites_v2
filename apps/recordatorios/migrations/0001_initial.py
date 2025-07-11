# Generated by Django 5.2.3 on 2025-06-25 14:45

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Recordatorio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('tipo', models.CharField(choices=[('POR_VENCER', 'Por Vencer'), ('VENCIDO', 'Vencido')], max_length=20, verbose_name='Tipo de Recordatorio')),
                ('mensaje', models.TextField(verbose_name='Mensaje de la notificación')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('leido', models.BooleanField(default=False, verbose_name='Leído')),
                ('enviado_por_correo', models.BooleanField(default=False, verbose_name='Enviado por Correo')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recordatorios', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Recordatorio',
                'verbose_name_plural': 'Recordatorios',
                'ordering': ['-fecha_creacion'],
            },
        ),
    ]
