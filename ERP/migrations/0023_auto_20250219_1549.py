# Generated by Django 3.2.10 on 2025-02-19 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ERP', '0022_student_fee_amount_custid'),
    ]

    operations = [
        migrations.AddField(
            model_name='student_fee_amount',
            name='discount',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='student_fee_amount',
            name='discount_percentage',
            field=models.CharField(default='0%', max_length=10),
        ),
        migrations.AddField(
            model_name='student_fee_amount',
            name='total_amount',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='student_fee_amount',
            name='original_amount',
            field=models.IntegerField(default=0),
        ),
    ]
