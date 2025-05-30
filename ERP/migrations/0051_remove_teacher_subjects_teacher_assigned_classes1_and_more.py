# Generated by Django 5.0.1 on 2025-03-11 10:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ERP', '0050_alter_studentadmission_classs_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacher',
            name='subjects',
        ),
        migrations.AddField(
            model_name='teacher',
            name='assigned_classes1',
            field=models.ManyToManyField(blank=True, related_name='teachers', to='ERP.class'),
        ),
        migrations.AddField(
            model_name='teacher',
            name='assigned_sections1',
            field=models.ManyToManyField(blank=True, related_name='teachers_sections', to='ERP.section'),
        ),
        migrations.AddField(
            model_name='teacher',
            name='assigned_subjects1',
            field=models.ManyToManyField(blank=True, related_name='teachers_subjects', to='ERP.subject'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='custid',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='teacher_register', to=settings.AUTH_USER_MODEL),
        ),
    ]
