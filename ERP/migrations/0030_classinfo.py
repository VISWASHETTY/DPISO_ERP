# Generated by Django 3.2.10 on 2025-02-24 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ERP', '0029_delete_payment'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_name', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
            ],
        ),
    ]
