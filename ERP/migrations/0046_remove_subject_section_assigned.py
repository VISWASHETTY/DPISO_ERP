# Generated by Django 5.0.1 on 2025-03-11 08:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ERP', '0045_class_section_subject'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subject',
            name='section_assigned',
        ),
    ]
