# Generated by Django 5.0.1 on 2025-03-10 08:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ERP', '0036_alter_studentpayment_student'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentpayment',
            name='student',
        ),
    ]
