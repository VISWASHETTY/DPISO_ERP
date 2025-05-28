from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils import timezone


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('accountant', 'Accountant'),
        ('student', 'Student'),
        ('non_teaching_staff', 'Non-Teaching Staff'),
    )
    role = models.CharField(max_length=30, choices=ROLE_CHOICES)

    groups = models.ManyToManyField(Group, related_name="customuser_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="customuser_permissions", blank=True)

#==============================SCHOOLS=============================================

class SchoolDetails(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    contact_number = models.CharField(max_length=15)
    email = models.EmailField()
    principal_name = models.CharField(max_length=255)
    established_year = models.PositiveIntegerField()
    logo = models.ImageField(upload_to='school_logos/', blank=True, null=True)
    description = models.TextField()
    custid=models.ForeignKey(CustomUser, on_delete=models.CASCADE , related_name='schools1', null=True)
    
    def __str__(self):
        return self.name
#==========================================================

class Class(models.Model):
    name = models.CharField(max_length=100)
    school = models.ForeignKey(SchoolDetails, on_delete=models.CASCADE, related_name='classes',null=True)

    def __str__(self):
        return self.name

class Section(models.Model):
    class_assigned = models.ForeignKey(Class, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    school = models.ForeignKey(SchoolDetails, on_delete=models.CASCADE, related_name='sections',null=True)


    def __str__(self):
        return f"{self.class_assigned.name} - {self.name}"

class Subject(models.Model):
    class_assigned = models.ForeignKey(Class, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    school = models.ForeignKey(SchoolDetails, on_delete=models.CASCADE, related_name='subjects',null=True)

    def __str__(self):
        return f"{self.name} ({self.class_assigned.name}"

class admin_fee_structure(models.Model):
    class_assigned=models.ForeignKey(Class, on_delete=models.CASCADE)
    amount=models.IntegerField()
    school = models.ForeignKey(SchoolDetails, on_delete=models.CASCADE, related_name='adminfeestructure',null=True)
class Meta:
    db_table="admin_fee_structure"


class StudentFeeRecord(models.Model):
    class_assigned = models.ForeignKey(Class, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    amount = models.IntegerField()

    def __str__(self):
        return f"{self.class_assigned.name} - {self.section.name} - {self.amount}"

#===================================================================================

from datetime import date

class studentadmission(models.Model):
    profile_photo = models.ImageField(upload_to="images/")
    enqno = models.CharField(max_length=50, default="")
    session = models.CharField(max_length=50, default="")
    registrationno = models.CharField(max_length=50, default="")
    classs = models.ForeignKey(Class, on_delete=models.CASCADE, null=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, null=True)
    srnno = models.CharField(max_length=50, default="")
    formno = models.CharField(max_length=50, default="")
    studenttype = models.CharField(max_length=50, default="")
    studentname = models.CharField(max_length=100, default="")
    gender = models.CharField(max_length=10, default="")
    dateofbirth = models.DateField(null=True, blank=True)
    aadharno = models.CharField(max_length=12, default="")
    house = models.CharField(max_length=150, default="")
    stream = models.CharField(max_length=50, default="")
    emil = models.EmailField(default="")
    previousyearattendance = models.TextField(default="")
    mothertongue = models.CharField(max_length=50, default="")
    adoptedchild = models.CharField(max_length=10, default="")
    minority = models.CharField(max_length=50, default="")
    specify = models.TextField(default="")
    nationality = models.CharField(max_length=50, default="")
    mediumofinstruction = models.CharField(max_length=50, default="")
    castecategory = models.CharField(max_length=50, default="")
    optionalsubject = models.TextField(default="", blank=True, null=True)
    offeredsubject = models.TextField(default="", blank=True, null=True)
    penno = models.CharField(max_length=50, default="")
    bloodgroup = models.CharField(max_length=5, default="")
    leftvision = models.CharField(max_length=10, default="")
    rightvision = models.CharField(max_length=10, default="")
    weight = models.CharField(max_length=50, default="")
    height = models.CharField(max_length=50, default="")
    weight1 = models.CharField(max_length=50, default="")
    height1 = models.CharField(max_length=50, default="")
    disability = models.CharField(max_length=50, default="")
    sportsactivity = models.TextField(default="")
    admissiondate = models.DateField(default=date.today, null=True, blank=True)
    bankname = models.CharField(max_length=100, default="")
    branchname = models.CharField(max_length=100, default="")
    accountno = models.CharField(max_length=50, default="")
    ifsccode = models.CharField(max_length=11, default="")
    address=models.CharField(max_length=150, default="")
    mbno=models.CharField(max_length=150, default="")
    custid=models.ForeignKey(CustomUser, on_delete=models.CASCADE , related_name='customss1', null=True)
    status=models.IntegerField(default=0)
    school = models.ForeignKey(SchoolDetails, on_delete=models.CASCADE, related_name='stdadmission',null=True)


    class Meta:
        db_table = "studentadmission"

from django.db import models

class EducationDetail(models.Model):
    
    stdid=models.ForeignKey(studentadmission, on_delete=models.CASCADE , related_name='workshifts', null=True)
    qualificationf1 = models.TextField(blank=True, null=True)
    specializationf1 = models.TextField(blank=True, null=True)
    institute_namef1 = models.TextField(blank=True, null=True)
    statef1 = models.TextField(blank=True, null=True)
    cityf1 = models.TextField(blank=True, null=True)

    qualificationf2 = models.TextField(blank=True, null=True)
    specializationf2 = models.TextField(blank=True, null=True)
    institute_namef2 = models.TextField(blank=True, null=True)
    statef2 = models.TextField(blank=True, null=True)
    cityf2 = models.TextField(blank=True, null=True)

    qualificationf3 = models.TextField(blank=True, null=True)
    specializationf3 = models.TextField(blank=True, null=True)
    institute_namef3 = models.TextField(blank=True, null=True)
    statef3 = models.TextField(blank=True, null=True)
    cityf3 = models.TextField(blank=True, null=True)

    qualificationf4 = models.TextField(blank=True, null=True)
    specializationf4 = models.TextField(blank=True, null=True)
    institute_namef4 = models.TextField(blank=True, null=True)
    statef4 = models.TextField(blank=True, null=True)
    cityf4 = models.TextField(blank=True, null=True)

    qualificationf5 = models.TextField(blank=True, null=True)
    specializationf5 = models.TextField(blank=True, null=True)
    institute_namef5 = models.TextField(blank=True, null=True)
    statef5 = models.TextField(blank=True, null=True)
    cityf5 = models.TextField(blank=True, null=True)


    qualificationm1 = models.TextField( blank=True, null=True)
    specializationm1 = models.TextField(blank=True, null=True)
    institute_namem1 = models.TextField(blank=True, null=True)
    statem1 = models.TextField( blank=True, null=True)
    citym1 = models.TextField(blank=True, null=True)

    qualificationm2 = models.TextField( blank=True, null=True)
    specializationm2 = models.TextField(max_length=200, blank=True, null=True)
    institute_namem2 = models.TextField(max_length=200, blank=True, null=True)
    statem2 = models.TextField(blank=True, null=True)
    citym2 = models.TextField(blank=True, null=True)

    qualificationm3 = models.TextField( blank=True, null=True)
    specializationm3 = models.TextField( blank=True, null=True)
    institute_namem3 = models.TextField( blank=True, null=True)
    statem3 = models.TextField( blank=True, null=True)
    citym3 = models.TextField( blank=True, null=True)

    qualificationm4 = models.TextField( blank=True, null=True)
    specializationm4 = models.TextField( blank=True, null=True)
    institute_namem4 = models.TextField( blank=True, null=True)
    statem4 = models.TextField( blank=True, null=True)
    citym4 = models.TextField(blank=True, null=True)

    qualificationm5 = models.TextField( blank=True, null=True)
    specializationm5 = models.TextField( blank=True, null=True)
    institute_namem5 = models.TextField( blank=True, null=True)
    statem5 = models.TextField(blank=True, null=True)
    citym5 = models.TextField(blank=True, null=True)

    qualificationg1 = models.TextField( blank=True, null=True)
    specializationg1 = models.TextField(blank=True, null=True)
    institute_nameg1 = models.TextField(blank=True, null=True)
    stateg1 = models.TextField( blank=True, null=True)
    cityg1 = models.TextField( blank=True, null=True)

    qualificationg2 = models.TextField( blank=True, null=True)
    specializationg2 = models.TextField(blank=True, null=True)
    institute_nameg2 = models.TextField( blank=True, null=True)
    stateg2 = models.TextField(blank=True, null=True)
    cityg2 = models.TextField(blank=True, null=True)

    qualificationg3 = models.TextField( blank=True, null=True)
    specializationg3 = models.TextField( blank=True, null=True)
    institute_nameg3 = models.TextField(blank=True, null=True)
    stateg3 = models.TextField(blank=True, null=True)
    cityg3 = models.TextField(blank=True, null=True)

    qualificationg4 = models.TextField(blank=True, null=True)
    specializationg4 = models.TextField( blank=True, null=True)
    institute_nameg4 = models.TextField( blank=True, null=True)
    stateg4 = models.TextField(blank=True, null=True)
    cityg4 = models.TextField(blank=True, null=True)

    qualificationg5 = models.TextField( blank=True, null=True)
    specializationg5 = models.TextField( blank=True, null=True)
    institute_nameg5 = models.TextField(blank=True, null=True)
    stateg5 = models.TextField(blank=True, null=True)
    cityg5 = models.TextField( blank=True, null=True)

    custid=models.ForeignKey(CustomUser, on_delete=models.CASCADE , related_name='customt1', null=True)
    status=models.IntegerField(default=0)
    school = models.ForeignKey(SchoolDetails, on_delete=models.CASCADE, related_name='edu',null=True)



class Meta :
    db_table="EducationDetail"


class Previousschooling(models.Model):
    schoolnameandaddress = models.CharField(max_length=100)
    classname = models.CharField(max_length=100)
    session = models.CharField(max_length=100)
    curriculum = models.CharField(max_length=50)
    subjects = models.CharField(max_length=50)
    stdid=models.ForeignKey(studentadmission, on_delete=models.CASCADE , related_name='workshifts1', null=True)
    custid=models.ForeignKey(CustomUser, on_delete=models.CASCADE , related_name='custom1', null=True)
    status=models.IntegerField(default=0)
    school = models.ForeignKey(SchoolDetails, on_delete=models.CASCADE, related_name='prevs',null=True)


    def __str__(self):
        return f"{self.schoolnameandaddress} - {self.session}"
    
from django.db import models

# Create your models here.
class FamilyDetails(models.Model):
    # Father Details
    stdid=models.ForeignKey(studentadmission, on_delete=models.CASCADE , related_name='workshifts2', null=True)
    father_name = models.CharField(max_length=255, default="")
    father_email = models.EmailField(default="")
    father_nationality = models.CharField(max_length=100, default="")
    father_occupation = models.CharField(max_length=100, default="")
    father_department = models.CharField(max_length=100, default="")
    father_designation = models.CharField(max_length=100, default="")
    father_name_of_office = models.CharField(max_length=255, default="")
    father_office_address = models.CharField(max_length=255, default="")
    father_office_contact_no = models.CharField(max_length=15, default="")
    father_aadhar_no = models.CharField(max_length=12, default="")
    father_pan_no = models.CharField(max_length=10, default="")
    father_annual_income = models.CharField(max_length=50, default="")
    father_mobile = models.CharField(max_length=15, default="")
    father_mobile2 = models.CharField(max_length=15, null=True, blank=True)
    father_religion = models.CharField(max_length=100, default="")
    father_caste = models.CharField(max_length=100, default="")
    father_marital_status = models.CharField(max_length=50, default="")
    
    # Mother Details
    mother_name = models.CharField(max_length=255, default="")
    mother_email = models.EmailField(default="")
    mother_nationality = models.CharField(max_length=100, default="")
    mother_occupation = models.CharField(max_length=100, default="")
    mother_department = models.CharField(max_length=100, default="")
    mother_designation = models.CharField(max_length=100, default="")
    mother_name_of_office = models.CharField(max_length=255, default="")
    mother_office_address = models.CharField(max_length=255, default="")
    mother_office_contact_no = models.CharField(max_length=15, default="")
    mother_aadhar_no = models.CharField(max_length=12, default="")
    mother_pan_no = models.CharField(max_length=10, default="")
    mother_annual_income = models.CharField(max_length=50, default="")
    mother_mobile = models.CharField(max_length=15, default="")
    mother_mobile2 = models.CharField(max_length=15, null=True, blank=True)
    mother_religion = models.CharField(max_length=100, default="")
    mother_caste = models.CharField(max_length=100, default="")
    mother_marital_status = models.CharField(max_length=50, default="")
    
    # Guardian Details
    guardian_name = models.CharField(max_length=255, default="")
    guardian_email = models.EmailField(default="")
    guardian_nationality = models.CharField(max_length=100, default="")
    guardian_occupation = models.CharField(max_length=100, default="")
    guardian_department = models.CharField(max_length=100, default="")
    guardian_designation = models.CharField(max_length=100, default="")
    guardian_name_of_office = models.CharField(max_length=255, default="")
    guardian_office_address = models.CharField(max_length=255, default="")
    guardian_office_contact_no = models.CharField(max_length=15, default="")
    guardian_aadhar_no = models.CharField(max_length=12, default="")
    guardian_pan_no = models.CharField(max_length=10, default="")
    guardian_annual_income = models.CharField(max_length=50, default="")
    guardian_mobile = models.CharField(max_length=15, default="")
    guardian_mobile2 = models.CharField(max_length=15, null=True, blank=True)
    guardian_religion = models.CharField(max_length=100, default="")
    guardian_caste = models.CharField(max_length=100, default="")
    guardian_marital_status = models.CharField(max_length=50, default="")
    guardian_relation = models.CharField(max_length=100, default="")
    guardian_address = models.CharField(max_length=255, default="")
    guardian_whatsapp = models.CharField(max_length=15, null=True, blank=True)
    guardian_place = models.CharField(max_length=100, default="")
    guardian_area = models.CharField(max_length=100, default="")
    guardian_location = models.CharField(max_length=255, default="")
    guardian_state = models.CharField(max_length=100, default="")
    guardian_city = models.CharField(max_length=100, default="")

    # Correspondence Address
    corres_address = models.CharField(max_length=255, default="")
    corres_mobile_no = models.CharField(max_length=15, default="")
    corres_whatsapp = models.CharField(max_length=15, null=True, blank=True)
    corres_place = models.CharField(max_length=100, default="")
    corres_area = models.CharField(max_length=100, default="")
    corres_location = models.CharField(max_length=255, default="")
    corres_state = models.CharField(max_length=100, default="")
    corres_city = models.CharField(max_length=100, default="")

    custid=models.ForeignKey(CustomUser, on_delete=models.CASCADE , related_name='customsd1', null=True)
    status=models.IntegerField(default=0)
    school = models.ForeignKey(SchoolDetails, on_delete=models.CASCADE, related_name='fds',null=True)



    def __str__(self):
        return f"Family Details: {self.father_name}, {self.mother_name}, {self.guardian_name}"





# Model for sibling details and document submission
class SiblingDocumentSubmission(models.Model):
    # Sibling Details
    stdid=models.ForeignKey(studentadmission, on_delete=models.CASCADE , related_name='workshifts3', null=True)
    name1 = models.CharField(max_length=100, blank=True, null=True)
    age1 = models.CharField(max_length=100,blank=True, null=True)
    gender1 = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')], blank=True, null=True)
    school1 = models.CharField(max_length=100, blank=True, null=True)
    class1 = models.CharField(max_length=100, blank=True, null=True)

    name2 = models.CharField(max_length=100, blank=True, null=True)
    age2 = models.CharField(max_length=100,blank=True, null=True)
    gender2 = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')], blank=True, null=True)
    school2 = models.CharField(max_length=100, blank=True, null=True)
    class2 = models.CharField(max_length=100, blank=True, null=True)

    name3 = models.CharField(max_length=100, blank=True, null=True)
    age3 = models.CharField(max_length=100,blank=True, null=True)
    gender3 = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')], blank=True, null=True)
    school3 = models.CharField(max_length=100, blank=True, null=True)
    class3 = models.CharField(max_length=100, blank=True, null=True)

    name4 = models.CharField(max_length=100, blank=True, null=True)
    age4 = models.CharField(max_length=100,blank=True, null=True)
    gender4 = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')], blank=True, null=True)
    school4 = models.CharField(max_length=100, blank=True, null=True)
    class4 = models.CharField(max_length=100, blank=True, null=True)

    name5 = models.CharField(max_length=100, blank=True, null=True)
    age5 = models.CharField(max_length=100,blank=True, null=True)
    gender5 = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')], blank=True, null=True)
    school5 = models.CharField(max_length=100, blank=True, null=True)
    class5 = models.CharField(max_length=100, blank=True, null=True)

    # Document Submission Details
    admission_form = models.CharField(max_length=10, choices=[('yes', 'Yes'), ('no', 'No'), ('partial', 'Partial'), ('na', 'N/A')], blank=True, null=True)
    admission_form_remarks = models.TextField(blank=True, null=True)

    school_leaving_certificate = models.CharField(max_length=10, choices=[('yes', 'Yes'), ('no', 'No'), ('partial', 'Partial'), ('na', 'N/A')], blank=True, null=True)
    school_leaving_certificate_remarks = models.TextField(blank=True, null=True)

    bonafide_certificate = models.CharField(max_length=10, choices=[('yes', 'Yes'), ('no', 'No'), ('partial', 'Partial'), ('na', 'N/A')], blank=True, null=True)
    bonafide_certificate_remarks = models.TextField(blank=True, null=True)

    birth_certificate = models.CharField(max_length=10, choices=[('yes', 'Yes'), ('no', 'No'), ('partial', 'Partial'), ('na', 'N/A')], blank=True, null=True)
    birth_certificate_remarks = models.TextField(blank=True, null=True)

    caste_certificate = models.CharField(max_length=10, choices=[('yes', 'Yes'), ('no', 'No'), ('partial', 'Partial'), ('na', 'N/A')], blank=True, null=True)
    caste_certificate_remarks = models.TextField(blank=True, null=True)

    all_documents = models.CharField(max_length=10, choices=[('yes', 'Yes'), ('no', 'No'), ('partial', 'Partial'), ('na', 'N/A')], blank=True, null=True)
    all_documents_remarks = models.TextField(blank=True, null=True)

    ration_card = models.CharField(max_length=10, choices=[('yes', 'Yes'), ('no', 'No'), ('partial', 'Partial'), ('na', 'N/A')], blank=True, null=True)
    ration_card_remarks = models.TextField(blank=True, null=True)

    student_adhar_certificate = models.CharField(max_length=10, choices=[('yes', 'Yes'), ('no', 'No'), ('partial', 'Partial'), ('na', 'N/A')], blank=True, null=True)
    student_adhar_certificate_remarks = models.TextField(blank=True, null=True)

    father_adhar_certificate = models.CharField(max_length=10, choices=[('yes', 'Yes'), ('no', 'No'), ('partial', 'Partial'), ('na', 'N/A')], blank=True, null=True)
    father_adhar_certificate_remarks = models.TextField(blank=True, null=True)

    mother_adhar_certificate = models.CharField(max_length=10, choices=[('yes', 'Yes'), ('no', 'No'), ('partial', 'Partial'), ('na', 'N/A')], blank=True, null=True)
    mother_adhar_certificate_remarks = models.TextField(blank=True, null=True)

    custid=models.ForeignKey(CustomUser, on_delete=models.CASCADE , related_name='customfdf1', null=True)
    status=models.IntegerField(default=0)
    school = models.ForeignKey(SchoolDetails, on_delete=models.CASCADE, related_name='siblings',null=True)



    def __str__(self):
        return f"Sibling and Document Submission for {self.name1} (Siblings info)"



class TransportFee(models.Model):
    
    distance = models.CharField(max_length=100)
    fee = models.DecimalField(max_digits=10, decimal_places=2)
    school = models.ForeignKey(SchoolDetails, on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):
        return f"{self.distance} - ₹{self.fee}"
    

class TransportInformation(models.Model):
    stdid=models.ForeignKey(studentadmission, on_delete=models.CASCADE , related_name='workshifts4', null=True)
    transport_available = models.CharField(max_length=3, default='no')
    bus_no = models.CharField(max_length=10)
    driver_name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    route = models.CharField(max_length=3)
    stoppage = models.CharField(max_length=10)
    fee1 = models.ForeignKey(TransportFee,models.CASCADE,blank=True,null=True)
    pick_up = models.CharField(max_length=100)
    drop_off = models.CharField(max_length=100)
    fee_category = models.CharField(max_length=20)
    fee_type = models.CharField(max_length=20)
    

    custid=models.ForeignKey(CustomUser, on_delete=models.CASCADE , related_name='customd1', null=True)
    status=models.IntegerField(default=0)
    school = models.ForeignKey(SchoolDetails, on_delete=models.CASCADE, related_name='transport',null=True)



    def __str__(self):
        return f'{self.bus_no} - {self.driver_name}'







class student_fee_Amount(models.Model):
    stdid = models.ForeignKey(studentadmission, on_delete=models.CASCADE, related_name="feeamount", null=True)
    classs = models.CharField(max_length=50)
    original_amount = models.IntegerField(default=0)
    discount = models.IntegerField(default=0)  # Discount applied
    discount_percentage = models.CharField(max_length=10, default="0%")  # Discount percentage
    total_amount = models.IntegerField(default=0)  # Amount after discount
    part1 = models.IntegerField(default=0)
    part2 = models.IntegerField(default=0)
    part3 = models.IntegerField(default=0)
    custid=models.ForeignKey(CustomUser, on_delete=models.CASCADE , related_name='custoddmd1', null=True)
    status=models.IntegerField(default=0)
    school = models.ForeignKey(SchoolDetails, on_delete=models.CASCADE, related_name='stdfee',null=True)



    def __str__(self):
        return f"Original: {self.original_amount} | Parts: {self.part1}, {self.part2}, {self.part3}"



class ClassInfo(models.Model):
    class_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.class_name
    


class StudentPayment(models.Model):
    student = models.ForeignKey(student_fee_Amount, on_delete=models.CASCADE, related_name="payments",null=True)
    admission_id = models.ForeignKey(studentadmission, on_delete=models.CASCADE, null=True)
    custid = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    fullname = models.CharField(max_length=100)
    fathername = models.CharField(max_length=100)
    amount1 = models.IntegerField(default=0)
    payment_date = models.DateTimeField(auto_now_add=True)
    admissionno=models.CharField(max_length=100,default="")
    mobilenumber=models.IntegerField(default=0)
    std_class=models.CharField(max_length=100,default="")
    

    def __str__(self):
        return f"{self.fullname} - {self.amount}"    
    


class Teacher(models.Model):
    custid = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='teacher_register', null=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status=models.IntegerField(default=0)

    # Many-to-Many relationships (renamed related_name to prevent conflicts)
    assigned_classes1 = models.ManyToManyField(Class, blank=True, related_name="teachers")
    assigned_sections1 = models.ManyToManyField(Section, blank=True, related_name="teachers_sections")
    assigned_subjects1 = models.ManyToManyField(Subject, blank=True, related_name="teachers_subjects")
    school = models.ForeignKey(SchoolDetails, on_delete=models.CASCADE, related_name='Teachers',null=True)
    profile = models.ImageField(upload_to="images/",default="",null=True,blank=True)
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
from django.contrib.auth.models import User 
from datetime import date

class AssignedClass(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="assignedfdegfregterclasses")
    custid = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="assigneddfdfdgdfgdfssscustomers")
    class_assigned = models.ForeignKey(Class, on_delete=models.CASCADE, null=True, blank=True, related_name="dffgtrytrytt")
    section = models.ForeignKey(Section, on_delete=models.CASCADE, null=True, blank=True, related_name="assignffdddddsections")
    assigned_at = models.DateTimeField(auto_now_add=True)
    school = models.ForeignKey(SchoolDetails, on_delete=models.CASCADE, related_name='assignedclasss',null=True)



class Meta :
    db_table="AssignedClass"


class StudentMarks(models.Model):
    student = models.ForeignKey(studentadmission, on_delete=models.CASCADE, related_name='marks')
    total_marks = models.IntegerField()
    date_entered = models.DateField(default=date.today)
    teacherid = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='teacherassignmarks',null=True)

    def __str__(self):
        return f"{self.student.studentname} - {self.total_marks}" 
    
#=====================================================
class Marks(models.Model):
    student = models.ForeignKey(studentadmission, on_delete=models.CASCADE,related_name='stdinfo')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE,related_name='subjectinfo')
    marks = models.IntegerField()

    def __str__(self):
        return f"{self.student.studentname} - {self.subject.name}: {self.marks}"

class exam(models.Model):
    examname=models.CharField(max_length=255,null=True, blank=True)
    school = models.ForeignKey(SchoolDetails, on_delete=models.CASCADE, related_name='exam',null=True)

class Meta :
    db_table="exam"
    


class StudentMarks1(models.Model):
    student = models.ForeignKey(studentadmission, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks = models.IntegerField()
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    exam = models.ForeignKey(exam, on_delete=models.CASCADE, blank=True, null=True)
    school = models.ForeignKey(SchoolDetails, on_delete=models.CASCADE, related_name='stdmarks1',null=True)

    def __str__(self):
        return f"{self.student.studentname} - {self.subject.name}: {self.marks}"    
    



class Attendance(models.Model):
    student = models.ForeignKey('studentadmission', on_delete=models.CASCADE)
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE)
    custid = models.ForeignKey('CustomUser', on_delete=models.CASCADE, null=True, blank=True)  # Add this field
    date = models.DateField(default=date.today)
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent')])

    def __str__(self):
        return f"{self.student.studentname} - {self.status}"


class StudentCredentials(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='plain_credentials')
    username = models.CharField(max_length=150)
    email = models.EmailField()
    password = models.CharField(max_length=255)  # Store plain password
    role = models.CharField(max_length=30, choices=CustomUser.ROLE_CHOICES)
    studentid = models.ForeignKey(studentadmission, on_delete=models.CASCADE , related_name='studentcredentials', null=True)
    school = models.ForeignKey(SchoolDetails, on_delete=models.CASCADE, related_name='stdcredits',null=True)
    def __str__(self):
        return f"{self.username} - {self.role}" 


class TeacherCredentials(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='plain_credentials1')
    username = models.CharField(max_length=150)
    email = models.EmailField()
    password = models.CharField(max_length=255)  # Store plain password
    role = models.CharField(max_length=30, choices=CustomUser.ROLE_CHOICES)
    teacherid = models.ForeignKey(Teacher, on_delete=models.CASCADE , related_name='teachercredentials', null=True)
    school = models.ForeignKey(SchoolDetails, on_delete=models.CASCADE, related_name='teacherpasswords',null=True)


    def __str__(self):
        return f"{self.username} - {self.role}"  


class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name + " - " + self.subject      




from django.utils.timezone import now

class LeaveRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='leave_requests')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='teacher_leaves', null=True, blank=True)
    subject = models.CharField(max_length=100)
    from_date = models.DateField()
    to_date = models.DateField()
    purpose = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Class and Section fields
    class_assigned = models.ForeignKey(Class, on_delete=models.CASCADE, null=True, blank=True)
    section_assigned = models.ForeignKey(Section, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.student.username} - {self.subject}"
    
class TeacherLeaveRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='teacher_leave_requests')
    subject = models.CharField(max_length=100)
    from_date = models.DateField()
    to_date = models.DateField()
    purpose = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.teacher.username} - {self.subject}"


# Notification model
class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}"
    

class ExtraSubjectMarks(models.Model):
    student = models.ForeignKey(studentadmission, on_delete=models.CASCADE)
    exam = models.ForeignKey(exam, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)  # ICT, GK, ROBOTICS, SPACE
    grade = models.CharField(max_length=5)  # e.g., A1, B2, etc.
    marks = models.IntegerField(default=0)  # Optional: store marks as well
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.studentname} - {self.subject}: {self.grade}"

class CoScholasticGrade(models.Model):
    GRADE_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C')
    ]
    grade = models.CharField(max_length=1, choices=GRADE_CHOICES, unique=True)
    grade_point = models.IntegerField()

    def __str__(self):
        return f"{self.grade} - {self.grade_point}"

class DisciplineGrade(models.Model):
    GRADE_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C')
    ]
    student = models.ForeignKey('studentadmission', on_delete=models.CASCADE)
    exam = models.ForeignKey('exam', on_delete=models.CASCADE)
    grade = models.CharField(max_length=1, choices=GRADE_CHOICES)
    
    def __str__(self):
        return f"{self.student.studentname} - {self.grade}"

class Remark(models.Model):
    student = models.ForeignKey('studentadmission', on_delete=models.CASCADE)
    exam = models.ForeignKey('exam', on_delete=models.CASCADE)
    remark = models.TextField()

    def __str__(self):
        return f"{self.student.studentname} - {self.remark[:30]}"

class ReportCardSignature(models.Model):
    student = models.ForeignKey('studentadmission', on_delete=models.CASCADE)
    exam = models.ForeignKey('exam', on_delete=models.CASCADE)
    teacher_signature = models.CharField(max_length=100)
    report_date = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.student.studentname} - {self.report_date.strftime('%d/%m/%Y')}"        


class SubjectMarksDetail(models.Model):
    student = models.ForeignKey('studentadmission', on_delete=models.CASCADE)
    exam = models.ForeignKey('exam', on_delete=models.CASCADE)
    subject = models.ForeignKey('subject', on_delete=models.CASCADE)

    pa = models.FloatField(default=0)   # Periodic Assessment out of 5
    se = models.FloatField(default=0)   # Subject Enrichment out of 5
    ma = models.FloatField(default=0)   # Multiple Assessments out of 5
    nb = models.FloatField(default=0)   # Notebook out of 5
    term = models.FloatField(default=0) # Term exam out of 80
    total = models.FloatField(default=0) # Calculated total out of 100

    def save(self, *args, **kwargs):
        # Automatically calculate the total before saving
        self.total = round(self.pa + self.se + self.ma + self.nb + self.term)
        super(SubjectMarksDetail, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.studentname} - {self.subject.name} - {self.total}"
    

class Circular(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    sent_to_students = models.BooleanField(default=False)
    sent_to_teachers = models.BooleanField(default=False)
    circular_image = models.ImageField(upload_to='images/', blank=True, null=True)
    school = models.ForeignKey(SchoolDetails, on_delete=models.CASCADE, related_name='circularlist',null=True)


    def __str__(self):
        return self.title    


#=====================================TEACHER DASHBOARD===================================

class teacherdashboardheading(models.Model):
    heading = models.CharField(max_length=255)
    status=models.IntegerField(default=0)
    school = models.ForeignKey(SchoolDetails, on_delete=models.CASCADE,null=True)
class Meta :
    db_table="teacherdashboardheading"

class teachersubmenu(models.Model):
    teacherid=models.ForeignKey('teacherdashboardheading', on_delete=models.CASCADE)
    title=models.CharField(max_length=255)
    urls=models.CharField(max_length=200)
    status = models.IntegerField(default=0)
    school = models.ForeignKey(SchoolDetails, on_delete=models.CASCADE,null=True)
class Meta : 
    db_table="teachersubmenu"
#==============================================================================================


from django.conf import settings    

class GalleryAlbum(models.Model):
    title = models.CharField(max_length=255)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    school = models.ForeignKey(SchoolDetails, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.title

class GalleryImage(models.Model):
    album = models.ForeignKey(GalleryAlbum, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="images/")
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    school = models.ForeignKey(SchoolDetails, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return f"Image in {self.album.title}"    
    

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    event_date = models.DateTimeField()
    venue = models.CharField(max_length=255)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    school = models.ForeignKey(SchoolDetails, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.title


class NonTeachingStaff(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=150)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    designation = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    school = models.ForeignKey(SchoolDetails, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.user.get_full_name()
    

class Driver(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    license_number = models.CharField(max_length=100)
    address = models.TextField()
    school = models.ForeignKey(SchoolDetails, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Route(models.Model):
    name = models.CharField(max_length=50)
    start_point = models.CharField(max_length=100)
    end_point = models.CharField(max_length=100)
    stops = models.TextField(help_text="Comma-separated list of stops")
    school = models.ForeignKey(SchoolDetails, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Transport(models.Model):
    school = models.ForeignKey(SchoolDetails, on_delete=models.CASCADE, related_name='transports')
    vechile_name = models.CharField(max_length=100)
    vechile_number = models.CharField(max_length=100)
    date_of_purchase = models.DateField()
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True)
    route = models.ForeignKey(Route, on_delete=models.SET_NULL, null=True, blank=True)


    def __str__(self):
        return f"{self.vechile_name} ({self.vechile_number})"


class TransportAttendance(models.Model):
    student = models.ForeignKey(studentadmission, on_delete=models.CASCADE)
    transport = models.ForeignKey(Transport, on_delete=models.CASCADE)
    school = models.ForeignKey(SchoolDetails, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent')])

    def __str__(self):
        return f"{self.student} - {self.date} - {self.status}"    
    

class TransportIssue(models.Model):
    student = models.ForeignKey(studentadmission, on_delete=models.CASCADE)
    school = models.ForeignKey(SchoolDetails, on_delete=models.CASCADE)
    date_reported = models.DateField(auto_now_add=True)
    issue_type = models.CharField(max_length=50, choices=[
        ('Bus Delay', 'Bus Delay'),
        ('Safety Concern', 'Safety Concern'),
        ('Missed Pickup', 'Missed Pickup'),
        ('No Transport Service', 'No Transport Service'),
        ('Other', 'Other')
    ])
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, default="Pending")
    transport = models.ForeignKey(Transport, on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):
        return f"{self.student.studentname} - {self.issue_type}"


class Message(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    attachment = models.FileField(upload_to='chat_attachments/', blank=True, null=True) 


    def __str__(self):
        return f'Message from {self.sender} to {self.recipient}'

class TypingStatus(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="typing_to")
    is_typing = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)


class ClassPhoto1(models.Model):
    school = models.ForeignKey(SchoolDetails, on_delete=models.CASCADE)
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    exam = models.ForeignKey(exam, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='class_photos/')

    def __str__(self):
        return f"{self.school} - {self.class_name} {self.section} - {self.exam}"    



class LeadSource(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)
    school = models.ForeignKey(SchoolDetails, on_delete=models.CASCADE, null=True, blank=True)  # ⬅️ Add this line


    def __str__(self):
        return self.name


class LeadStatus(models.Model):
    name = models.CharField(max_length=100)
    text_color = models.CharField(max_length=20, default="#000000")
    bg_color = models.CharField(max_length=20, default="#FFFFFF")
    created_at = models.DateTimeField(default=timezone.now)
    school = models.ForeignKey(SchoolDetails, on_delete=models.CASCADE, null=True, blank=True)  # ⬅️ Add this line


    def __str__(self):
        return self.name


from django.db import models

GENDER_CHOICES = [
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other'),
]

class Lead(models.Model):
    admission_class = models.CharField(max_length=50)
    source = models.ForeignKey(LeadSource, on_delete=models.CASCADE, null=True, blank=True)
    referred_by = models.CharField(max_length=100, blank=True, null=True)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    mobile = models.CharField(max_length=15)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    dob = models.DateField(null=True, blank=True)

    # Parent details
    mother_name = models.CharField(max_length=100, blank=True)
    mother_qualification = models.CharField(max_length=100, blank=True)
    mother_res_address = models.TextField(blank=True)
    mother_occupation = models.CharField(max_length=100, blank=True)
    mother_official_address = models.TextField(blank=True)
    mother_income = models.CharField(max_length=100, blank=True)
    mother_email = models.EmailField(blank=True)
    mother_mobile = models.CharField(max_length=15, blank=True)

    father_name = models.CharField(max_length=100, blank=True)
    father_qualification = models.CharField(max_length=100, blank=True)
    father_res_address = models.TextField(blank=True)
    father_occupation = models.CharField(max_length=100, blank=True)
    father_official_address = models.TextField(blank=True)
    father_income = models.CharField(max_length=100, blank=True)
    father_email = models.EmailField(blank=True)
    father_mobile = models.CharField(max_length=15, blank=True)

    nationality = models.CharField(max_length=50, blank=True)
    religion = models.CharField(max_length=50, blank=True)
    category = models.CharField(max_length=50, blank=True)
    aadhar_no = models.CharField(max_length=20, blank=True)

    last_school_name = models.CharField(max_length=200, blank=True)
    last_attended_class = models.CharField(max_length=50, blank=True)
    last_school_affiliated_to = models.CharField(max_length=200, blank=True)

    status = models.ForeignKey(LeadStatus, on_delete=models.CASCADE, null=True, blank=True)
    remark = models.TextField(blank=True)
    created_by = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    scheduled_at = models.DateTimeField(blank=True, null=True)
    school = models.ForeignKey(SchoolDetails, on_delete=models.CASCADE, null=True, blank=True)
    assigned_to = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    

class TimeTableEntry(models.Model):
    WEEKDAYS = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
    ]

    PERIOD_CHOICES = [(f'Period {i}', f'Period {i}') for i in range(1, 9)]

    school = models.ForeignKey(SchoolDetails, on_delete=models.CASCADE)
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    weekday = models.CharField(max_length=10, choices=WEEKDAYS)
    period = models.CharField(max_length=20, choices=PERIOD_CHOICES)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    school = models.ForeignKey(SchoolDetails, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('class_name', 'section', 'weekday', 'period', 'school')
