# Generated by Django 5.0.1 on 2025-03-11 04:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ERP', '0039_studentmarks'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentmarks',
            name='teacherid',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='teacherassignmarks', to='ERP.teacher'),
        ),
    ]
