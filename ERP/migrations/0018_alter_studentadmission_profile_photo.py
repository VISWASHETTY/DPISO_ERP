# Generated by Django 3.2.10 on 2025-02-18 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ERP', '0017_studentadmission_profile_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentadmission',
            name='profile_photo',
            field=models.ImageField(upload_to='images/'),
        ),
    ]
