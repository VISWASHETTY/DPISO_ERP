# Generated by Django 5.0.1 on 2025-04-04 05:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ERP', '0087_exam_school'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignedclass',
            name='school',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assignedclasss', to='ERP.schooldetails'),
        ),
    ]
