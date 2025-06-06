# Generated by Django 3.2.10 on 2025-03-26 04:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ERP', '0072_teacherleaverequest'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExtraSubjectMarks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=100)),
                ('grade', models.CharField(max_length=5)),
                ('marks', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ERP.exam')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ERP.studentadmission')),
            ],
        ),
    ]
