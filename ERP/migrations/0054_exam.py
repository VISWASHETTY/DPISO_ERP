# Generated by Django 5.0.1 on 2025-03-13 03:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ERP', '0053_studentmarks1'),
    ]

    operations = [
        migrations.CreateModel(
            name='exam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('examname', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
    ]
