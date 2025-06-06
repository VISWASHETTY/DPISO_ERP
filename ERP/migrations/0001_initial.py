# Generated by Django 3.2.10 on 2025-02-11 05:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FamilyDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('father_name', models.CharField(default='', max_length=255)),
                ('father_email', models.EmailField(default='', max_length=254)),
                ('father_nationality', models.CharField(default='', max_length=100)),
                ('father_occupation', models.CharField(default='', max_length=100)),
                ('father_department', models.CharField(default='', max_length=100)),
                ('father_designation', models.CharField(default='', max_length=100)),
                ('father_name_of_office', models.CharField(default='', max_length=255)),
                ('father_office_address', models.CharField(default='', max_length=255)),
                ('father_office_contact_no', models.CharField(default='', max_length=15)),
                ('father_aadhar_no', models.CharField(default='', max_length=12)),
                ('father_pan_no', models.CharField(default='', max_length=10)),
                ('father_annual_income', models.DecimalField(decimal_places=2, default='', max_digits=10)),
                ('father_mobile', models.CharField(default='', max_length=15)),
                ('father_mobile2', models.CharField(blank=True, max_length=15, null=True)),
                ('father_religion', models.CharField(default='', max_length=100)),
                ('father_caste', models.CharField(default='', max_length=100)),
                ('father_marital_status', models.CharField(default='', max_length=50)),
                ('mother_name', models.CharField(default='', max_length=255)),
                ('mother_email', models.EmailField(default='', max_length=254)),
                ('mother_nationality', models.CharField(default='', max_length=100)),
                ('mother_occupation', models.CharField(default='', max_length=100)),
                ('mother_department', models.CharField(default='', max_length=100)),
                ('mother_designation', models.CharField(default='', max_length=100)),
                ('mother_name_of_office', models.CharField(default='', max_length=255)),
                ('mother_office_address', models.CharField(default='', max_length=255)),
                ('mother_office_contact_no', models.CharField(default='', max_length=15)),
                ('mother_aadhar_no', models.CharField(default='', max_length=12)),
                ('mother_pan_no', models.CharField(default='', max_length=10)),
                ('mother_annual_income', models.DecimalField(decimal_places=2, default='', max_digits=10)),
                ('mother_mobile', models.CharField(default='', max_length=15)),
                ('mother_mobile2', models.CharField(blank=True, max_length=15, null=True)),
                ('mother_religion', models.CharField(default='', max_length=100)),
                ('mother_caste', models.CharField(default='', max_length=100)),
                ('mother_marital_status', models.CharField(default='', max_length=50)),
                ('guardian_name', models.CharField(default='', max_length=255)),
                ('guardian_email', models.EmailField(default='', max_length=254)),
                ('guardian_nationality', models.CharField(default='', max_length=100)),
                ('guardian_occupation', models.CharField(default='', max_length=100)),
                ('guardian_department', models.CharField(default='', max_length=100)),
                ('guardian_designation', models.CharField(default='', max_length=100)),
                ('guardian_name_of_office', models.CharField(default='', max_length=255)),
                ('guardian_office_address', models.CharField(default='', max_length=255)),
                ('guardian_office_contact_no', models.CharField(default='', max_length=15)),
                ('guardian_aadhar_no', models.CharField(default='', max_length=12)),
                ('guardian_pan_no', models.CharField(default='', max_length=10)),
                ('guardian_annual_income', models.DecimalField(decimal_places=2, default='', max_digits=10)),
                ('guardian_mobile', models.CharField(default='', max_length=15)),
                ('guardian_mobile2', models.CharField(blank=True, max_length=15, null=True)),
                ('guardian_religion', models.CharField(default='', max_length=100)),
                ('guardian_caste', models.CharField(default='', max_length=100)),
                ('guardian_marital_status', models.CharField(default='', max_length=50)),
                ('guardian_relation', models.CharField(default='', max_length=100)),
                ('guardian_address', models.CharField(default='', max_length=255)),
                ('guardian_whatsapp', models.CharField(blank=True, max_length=15, null=True)),
                ('guardian_place', models.CharField(default='', max_length=100)),
                ('guardian_area', models.CharField(default='', max_length=100)),
                ('guardian_location', models.CharField(default='', max_length=255)),
                ('guardian_state', models.CharField(default='', max_length=100)),
                ('guardian_city', models.CharField(default='', max_length=100)),
                ('corres_address', models.CharField(default='', max_length=255)),
                ('corres_mobile_no', models.CharField(default='', max_length=15)),
                ('corres_whatsapp', models.CharField(blank=True, max_length=15, null=True)),
                ('corres_place', models.CharField(default='', max_length=100)),
                ('corres_area', models.CharField(default='', max_length=100)),
                ('corres_location', models.CharField(default='', max_length=255)),
                ('corres_state', models.CharField(default='', max_length=100)),
                ('corres_city', models.CharField(default='', max_length=100)),
            ],
        ),
    ]
