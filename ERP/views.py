
from django.http import JsonResponse
from django.db.models import Max, Min
from django.shortcuts import render,redirect
from django.http import JsonResponse, HttpResponse
from .models import studentadmission, EducationDetail,FamilyDetails,Previousschooling,SiblingDocumentSubmission,TransportInformation,CustomUser,admin_fee_structure,student_fee_Amount,StudentPayment,Teacher,AssignedClass
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.hashers import make_password
from django.http import Http404
from datetime import datetime
import os
from io import BytesIO
from xhtml2pdf import pisa
import razorpay
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
import pandas as pd
from django.contrib.auth.hashers import make_password
from django.utils.crypto import get_random_string 
from .models import *
from django.utils.timezone import now
from django.contrib import messages
import calendar

#school==============================================================

# def show(request,pk):
#     pk=pk
#     return render(request,'show.html',{'pk':pk})

def add_school_details(request):
    if request.method == "POST":
        username = request.POST.get('username', None)
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        role = request.POST.get('role', 'student')

        if not username:
            while True:
                username = f"user_{get_random_string(6)}"
                if not CustomUser.objects.filter(username=username).exists():
                    break  
        if not email:
            email = f"{username}@example.com"
        if not password:
            password = get_random_string(8)

        hashed_password = make_password(password)

        # Create the user
        user = CustomUser.objects.create(
            username=username,
            email=email,
            password=hashed_password,
            role=role
        )
        name = request.POST.get("name")
        address = request.POST.get("address")
        contact_number = request.POST.get("contact_number")
        email = request.POST.get("email")
        principal_name = request.POST.get("principal_name")
        established_year = request.POST.get("established_year")
        description = request.POST.get("description")
        logo = request.FILES.get("logo")  # Handling file upload

        SchoolDetails.objects.create(
            name=name,
            address=address,
            contact_number=contact_number,
            email=email,
            principal_name=principal_name,
            established_year=established_year,
            description=description,
            logo=logo,
            custid=user
        )

        return redirect("add_school_details")  

    return render(request, "add_school.html")

#==============================================================================

def insert_student_admission(request):
    try:
        a1 = SchoolDetails.objects.get(custid=request.user)
    except SchoolDetails.DoesNotExist:
        messages.error(request, "School details not found!")
        return redirect('admin_dashboard')  # Redirect if school is not set up
    
    trans = TransportFee.objects.filter(school=a1)
    fees = admin_fee_structure.objects.filter(school=a1)
    students = studentadmission.objects.all()
    next_admission_id = (studentadmission.objects.aggregate(Max('id'))['id__max'] or 0) + 1

    bus_numbers = Transport.objects.filter(school=a1).values_list('vechile_number', flat=True).distinct()
    routes = Route.objects.filter(school=a1)

    if request.method == 'POST':
        username = request.POST.get('username', None)
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        role = request.POST.get('role', 'student')

        if not username:
            while True:
                username = f"user_{get_random_string(6)}"
                if not CustomUser.objects.filter(username=username).exists():
                    break  
        if not email:
            email = f"{username}@example.com"
        if not password:
            password = get_random_string(8)

        hashed_password = make_password(password)

        # Create the user
        user = CustomUser.objects.create(
            username=username,
            email=email,
            password=hashed_password,
            role=role
        )

        profile_photo = request.FILES.get('profile_photo')
        enqno = request.POST.get('enqno')
        session = request.POST.get('session')
        registrationno = request.POST.get('registrationno')

        # Get Class and Section IDs
        class_id = request.POST.get('classs')
        section_id = request.POST.get('section')

        if not class_id or not section_id:
            return JsonResponse({"message": "Class and Section are required."}, status=400)

        try:
            class_obj = Class.objects.get(id=class_id,school=a1)
            section_obj = Section.objects.get(id=section_id,school=a1)
        except Class.DoesNotExist:
            return JsonResponse({"message": "Invalid Class ID."}, status=400)
        except Section.DoesNotExist:
            return JsonResponse({"message": "Invalid Section ID."}, status=400)

        srnno = request.POST.get('srnno')
        formno = request.POST.get('formno')
        studenttype = request.POST.get('studenttype')
        studentname = request.POST.get('studentname')
        gender = request.POST.get('gender')
        dateofbirth = request.POST.get('dateofbirth')
        aadharno = request.POST.get('aadharno')
        house = request.POST.get('house')
        stream = request.POST.get('stream')
        email = request.POST.get('emil')
        previousyearattendance = request.POST.get('previousyearattendance')
        mothertongue = request.POST.get('mothertongue')
        adoptedchild = request.POST.get('adoptedchild')
        minority = request.POST.get('minority')
        specify = request.POST.get('specify')
        nationality = request.POST.get('nationality')
        mediumofinstruction = request.POST.get('mediumofinstruction')
        castecategory = request.POST.get('castecategory')
        optionalsubject = request.POST.get('optionalsubject')
        offeredsubject = request.POST.get('offeredsubject')
        penno = request.POST.get('penno')
        bloodgroup = request.POST.get('bloodgroup')
        leftvision = request.POST.get('leftvision')
        rightvision = request.POST.get('rightvision')
        weight = request.POST.get('weight')
        height = request.POST.get('height')
        weight1 = request.POST.get('weight1')
        height1 = request.POST.get('height1')
        disability = request.POST.get('disability')
        sportsactivity = request.POST.get('sportsactivity')
        admissiondate = request.POST.get('admissiondate')
        bankname = request.POST.get('bankname')
        branchname = request.POST.get('branchname')
        accountno = request.POST.get('accountno')
        ifsccode = request.POST.get('ifsccode')

        if admissiondate:
            try:
                # Convert to YYYY-MM-DD format
                admissiondate = datetime.strptime(admissiondate, '%Y-%m-%d').date()
            except ValueError:
                admissiondate = None
        else:
            admissiondate = None

        if dateofbirth:
            try:
                # Convert to YYYY-MM-DD format
                dateofbirth = datetime.strptime(dateofbirth, '%Y-%m-%d').date()
            except ValueError:
                dateofbirth = None
        else:
            dateofbirth = None    



        # Create Student Admission
        student = studentadmission.objects.create(
            profile_photo=profile_photo,
            enqno=enqno,
            session=session,
            registrationno=registrationno,
            classs=class_obj,  # Storing Class ID
            section=section_obj,  # Storing Section ID
            srnno=srnno,
            formno=formno,
            studenttype=studenttype,
            studentname=studentname,
            gender=gender,
            dateofbirth=dateofbirth,
            aadharno=aadharno,
            house=house,
            stream=stream,
            emil=email,
            previousyearattendance=previousyearattendance,
            mothertongue=mothertongue,
            adoptedchild=adoptedchild,
            minority=minority,
            specify=specify,
            nationality=nationality,
            mediumofinstruction=mediumofinstruction,
            castecategory=castecategory,
            optionalsubject=optionalsubject,
            offeredsubject=offeredsubject,
            penno=penno,
            bloodgroup=bloodgroup,
            leftvision=leftvision,
            rightvision=rightvision,
            weight=weight,
            height=height,
            weight1=weight1,
            height1=height1,
            disability=disability,
            sportsactivity=sportsactivity,
            admissiondate=admissiondate,
            bankname=bankname,
            branchname=branchname,
            accountno=accountno,
            ifsccode=ifsccode,
            custid=user,
            school=a1
        )
        StudentCredentials.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            password=password,
            role=user.role,
            studentid=student,
            school=a1
        )

        # Get Fee Amount from Admin Fee Structure
        try:
            fee_structure = admin_fee_structure.objects.get(class_assigned=class_obj)
            amount = fee_structure.amount  
        except admin_fee_structure.DoesNotExist:
            return JsonResponse({"message": "Fee structure not found for this class."}, status=400)

        category = request.POST.get("category", None)

        # Define Discount Percentage
        percentage_map = {
            "admin": (0.50, "50%"),
            "staff": (0.25, "25%"),
            "normal": (0.10, "10%")
        }

        discount_percentage_value, discount_percentage_label = percentage_map.get(category, (0, "0%"))

        discount = int(amount * discount_percentage_value)
        total_amount = amount - discount

        # Split Total Amount into 3 Parts
        part = total_amount // 3
        remainder = total_amount % 3
        parts = [part, part, part]

        for i in range(remainder):
            parts[i] += 1

        # Save Fee Details
        student_fee_Amount.objects.create(
            classs=class_obj,  # Storing Class ID
            stdid=student,
            original_amount=amount,  
            discount=discount, 
            discount_percentage=discount_percentage_label, 
            total_amount=total_amount,  
            part1=parts[0],
            part2=parts[1],
            part3=parts[2],
            custid=user,
            school=a1
        )
        qualificationf1 = request.POST.get("qualificationf1")
        specializationf1 = request.POST.get("specializationf1")
        institute_namef1 = request.POST.get("institute_namef1")
        statef1 = request.POST.get("statef1")
        cityf1 = request.POST.get("cityf1")

        qualificationf2 = request.POST.get("qualificationf2")
        specializationf2 = request.POST.get("specializationf2")
        institute_namef2 = request.POST.get("institute_namef2")
        statef2 = request.POST.get("statef2")
        cityf2 = request.POST.get("cityf2")

        qualificationf3 = request.POST.get("qualificationf3")
        specializationf3 = request.POST.get("specializationf3")
        institute_namef3 = request.POST.get("institute_namef3")
        statef3 = request.POST.get("statef3")
        cityf3 = request.POST.get("cityf3")

        qualificationf4 = request.POST.get("qualificationf4")
        specializationf4 = request.POST.get("specializationf4")
        institute_namef4 = request.POST.get("institute_namef4")
        statef4 = request.POST.get("statef4")
        cityf4 = request.POST.get("cityf4")

        qualificationf5 = request.POST.get("qualificationf5")
        specializationf5 = request.POST.get("specializationf5")
        institute_namef5 = request.POST.get("institute_namef5")
        statef5 = request.POST.get("statef5")
        cityf5 = request.POST.get("cityf5")

        qualificationm1 = request.POST.get("qualificationm1")
        specializationm1 = request.POST.get("specializationm1")
        institute_namem1 = request.POST.get("institute_namem1")
        statem1 = request.POST.get("statem1")
        citym1 = request.POST.get("citym1")

        qualificationm2 = request.POST.get("qualificationm2")
        specializationm2 = request.POST.get("specializationm2")
        institute_namem2 = request.POST.get("institute_namem2")
        statem2 = request.POST.get("statem2")
        citym2 = request.POST.get("citym2")

        qualificationm3 = request.POST.get("qualificationm3")
        specializationm3 = request.POST.get("specializationm3")
        institute_namem3 = request.POST.get("institute_namem3")
        statem3 = request.POST.get("statem3")
        citym3 = request.POST.get("citym3")

        qualificationm4 = request.POST.get("qualificationm4")
        specializationm4 = request.POST.get("specializationm4")
        institute_namem4 = request.POST.get("institute_namem4")
        statem4 = request.POST.get("statem4")
        citym4 = request.POST.get("citym4")

        qualificationm5 = request.POST.get("qualificationm5")
        specializationm5 = request.POST.get("specializationm5")
        institute_namem5 = request.POST.get("institute_namem5")
        statem5 = request.POST.get("statem5")
        citym5 = request.POST.get("citym5")

        qualificationg1 = request.POST.get("qualificationg1")
        specializationg1 = request.POST.get("specializationg1")
        institute_nameg1 = request.POST.get("institute_nameg1")
        stateg1 = request.POST.get("stateg1")
        cityg1 = request.POST.get("cityg1")

        qualificationg2 = request.POST.get("qualificationg2")
        specializationg2 = request.POST.get("specializationg2")
        institute_nameg2 = request.POST.get("institute_nameg2")
        stateg2 = request.POST.get("stateg2")
        cityg2 = request.POST.get("cityg2")

        qualificationg3 = request.POST.get("qualificationg3")
        specializationg3 = request.POST.get("specializationg3")
        institute_nameg3 = request.POST.get("institute_nameg3")
        stateg3 = request.POST.get("stateg3")
        cityg3 = request.POST.get("cityg3")

        qualificationg4 = request.POST.get("qualificationg4")
        specializationg4 = request.POST.get("specializationg4")
        institute_nameg4 = request.POST.get("institute_nameg4")
        stateg4 = request.POST.get("stateg4")
        cityg4 = request.POST.get("cityg4")

        qualificationg5 = request.POST.get("qualificationg5")
        specializationg5 = request.POST.get("specializationg5")
        institute_nameg5 = request.POST.get("institute_nameg5")
        stateg5 = request.POST.get("stateg5")
        cityg5 = request.POST.get("cityg5")
        
        EducationDetail.objects.create(
            qualificationf1=qualificationf1, specializationf1=specializationf1, institute_namef1=institute_namef1, statef1=statef1, cityf1=cityf1,
            qualificationf2=qualificationf2, specializationf2=specializationf2, institute_namef2=institute_namef2, statef2=statef2, cityf2=cityf2,
            qualificationf3=qualificationf3, specializationf3=specializationf3, institute_namef3=institute_namef3, statef3=statef3, cityf3=cityf3,
            qualificationf4=qualificationf4, specializationf4=specializationf4, institute_namef4=institute_namef4, statef4=statef4, cityf4=cityf4,
            qualificationf5=qualificationf5, specializationf5=specializationf5, institute_namef5=institute_namef5, statef5=statef5, cityf5=cityf5,
            qualificationm1=qualificationm1, specializationm1=specializationm1, institute_namem1=institute_namem1, statem1=statem1, citym1=citym1,
            qualificationm2=qualificationm2, specializationm2=specializationm2, institute_namem2=institute_namem2, statem2=statem2, citym2=citym2,
            qualificationm3=qualificationm3, specializationm3=specializationm3, institute_namem3=institute_namem3, statem3=statem3, citym3=citym3,
            qualificationm4=qualificationm4, specializationm4=specializationm4, institute_namem4=institute_namem4, statem4=statem4, citym4=citym4,
            qualificationm5=qualificationm5, specializationm5=specializationm5, institute_namem5=institute_namem5, statem5=statem5, citym5=citym5,
            qualificationg1=qualificationg1, specializationg1=specializationg1, institute_nameg1=institute_nameg1, stateg1=stateg1, cityg1=cityg1,
            qualificationg2=qualificationg2, specializationg2=specializationg2, institute_nameg2=institute_nameg2, stateg2=stateg2, cityg2=cityg2,
            qualificationg3=qualificationg3, specializationg3=specializationg3, institute_nameg3=institute_nameg3, stateg3=stateg3, cityg3=cityg3,
            qualificationg4=qualificationg4, specializationg4=specializationg4, institute_nameg4=institute_nameg4, stateg4=stateg4, cityg4=cityg4,
            qualificationg5=qualificationg5, specializationg5=specializationg5, institute_nameg5=institute_nameg5, stateg5=stateg5, cityg5=cityg5,stdid=student,custid=user, school=a1,
        )
        school_names = request.POST.getlist('schoolnameandaddress[]')
        class_names = request.POST.getlist('classname[]')
        sessions = request.POST.getlist('session[]')
        curriculums = request.POST.getlist('curriculum[]')
        subjects = request.POST.getlist('subjects[]')
        for school_name, class_name, session, curriculum, subject in zip(school_names, class_names, sessions, curriculums, subjects):
            if school_name:  
                Previousschooling.objects.create(
                    stdid=student,
                    schoolnameandaddress=school_name,
                    classname=class_name,
                    session=session,
                    curriculum=curriculum,
                    subjects=subject,
                    custid=user,
                    school=a1
                )

        father_name = request.POST.get('father_name')
        father_email = request.POST.get('father_email')
        father_nationality = request.POST.get('father_nationality')
        father_occupation = request.POST.get('father_occupation')
        father_department = request.POST.get('father_department')
        father_designation = request.POST.get('father_designation')
        father_name_of_office = request.POST.get('father_name_of_office')
        father_office_address = request.POST.get('father_office_address')
        father_office_contact_no = request.POST.get('father_office_contact_no')
        father_aadhar_no = request.POST.get('father_aadhar_no')
        father_pan_no = request.POST.get('father_pan_no')
        father_annual_income = request.POST.get('father_annual_income')
        father_mobile = request.POST.get('father_mobile')
        father_mobile2 = request.POST.get('father_mobile2')
        father_religion = request.POST.get('father_religion')
        father_caste = request.POST.get('father_caste')
        father_marital_status = request.POST.get('father_marital_status')

        mother_name = request.POST.get('mother_name')
        mother_email = request.POST.get('mother_email')
        mother_nationality = request.POST.get('mother_nationality')
        mother_occupation = request.POST.get('mother_occupation')
        mother_department = request.POST.get('mother_department')
        mother_designation = request.POST.get('mother_designation')
        mother_name_of_office = request.POST.get('mother_name_of_office')
        mother_office_address = request.POST.get('mother_office_address')
        mother_office_contact_no = request.POST.get('mother_office_contact_no')
        mother_aadhar_no = request.POST.get('mother_aadhar_no')
        mother_pan_no = request.POST.get('mother_pan_no')
        mother_annual_income = request.POST.get('mother_annual_income')
        mother_mobile = request.POST.get('mother_mobile')
        mother_mobile2 = request.POST.get('mother_mobile2')
        mother_religion = request.POST.get('mother_religion')
        mother_caste = request.POST.get('mother_caste')
        mother_marital_status = request.POST.get('mother_marital_status')

        guardian_name = request.POST.get('guardian_name')
        guardian_email = request.POST.get('guardian_email')
        guardian_nationality = request.POST.get('guardian_nationality')
        guardian_occupation = request.POST.get('guardian_occupation')
        guardian_department = request.POST.get('guardian_department')
        guardian_designation = request.POST.get('guardian_designation')
        guardian_name_of_office = request.POST.get('guardian_name_of_office')
        guardian_office_address = request.POST.get('guardian_office_address')
        guardian_office_contact_no = request.POST.get('guardian_office_contact_no')
        guardian_aadhar_no = request.POST.get('guardian_aadhar_no')
        guardian_pan_no = request.POST.get('guardian_pan_no')
        guardian_annual_income = request.POST.get('guardian_annual_income')
        guardian_mobile = request.POST.get('guardian_mobile')
        guardian_mobile2 = request.POST.get('guardian_mobile2')
        guardian_religion = request.POST.get('guardian_religion')
        guardian_caste = request.POST.get('guardian_caste')
        guardian_marital_status = request.POST.get('guardian_marital_status')
        guardian_relation = request.POST.get('guardian_relation')
        guardian_address = request.POST.get('guardian_address')
        guardian_whatsapp = request.POST.get('guardian_whatsapp')
        guardian_place = request.POST.get('guardian_place')
        guardian_area = request.POST.get('guardian_area')
        guardian_location = request.POST.get('guardian_location')
        guardian_state = request.POST.get('guardian_state')
        guardian_city = request.POST.get('guardian_city')

        corres_address = request.POST.get('corres_address')
        corres_mobile_no = request.POST.get('corres_mobile_no')
        corres_whatsapp = request.POST.get('corres_whatsapp')
        corres_place = request.POST.get('corres_place')
        corres_area = request.POST.get('corres_area')
        corres_location = request.POST.get('corres_location')
        corres_state = request.POST.get('corres_state')
        corres_city = request.POST.get('corres_city')

        FamilyDetails.objects.create(
            stdid=student,
            father_name=father_name,
            father_email=father_email,
            father_nationality=father_nationality,
            father_occupation=father_occupation,
            father_department=father_department,
            father_designation=father_designation,
            father_name_of_office=father_name_of_office,
            father_office_address=father_office_address,
            father_office_contact_no=father_office_contact_no,
            father_aadhar_no=father_aadhar_no,
            father_pan_no=father_pan_no,
            father_annual_income=father_annual_income,
            father_mobile=father_mobile,
            father_mobile2=father_mobile2,
            father_religion=father_religion,
            father_caste=father_caste,
            father_marital_status=father_marital_status,

            mother_name=mother_name,
            mother_email=mother_email,
            mother_nationality=mother_nationality,
            mother_occupation=mother_occupation,
            mother_department=mother_department,
            mother_designation=mother_designation,
            mother_name_of_office=mother_name_of_office,
            mother_office_address=mother_office_address,
            mother_office_contact_no=mother_office_contact_no,
            mother_aadhar_no=mother_aadhar_no,
            mother_pan_no=mother_pan_no,
            mother_annual_income=mother_annual_income,
            mother_mobile=mother_mobile,
            mother_mobile2=mother_mobile2,
            mother_religion=mother_religion,
            mother_caste=mother_caste,
            mother_marital_status=mother_marital_status,

            guardian_name=guardian_name,
            guardian_email=guardian_email,
            guardian_nationality=guardian_nationality,
            guardian_occupation=guardian_occupation,
            guardian_department=guardian_department,
            guardian_designation=guardian_designation,
            guardian_name_of_office=guardian_name_of_office,
            guardian_office_address=guardian_office_address,
            guardian_office_contact_no=guardian_office_contact_no,
            guardian_aadhar_no=guardian_aadhar_no,
            guardian_pan_no=guardian_pan_no,
            guardian_annual_income=guardian_annual_income,
            guardian_mobile=guardian_mobile,
            guardian_mobile2=guardian_mobile2,
            guardian_religion=guardian_religion,
            guardian_caste=guardian_caste,
            guardian_marital_status=guardian_marital_status,
            guardian_relation=guardian_relation,
            guardian_address=guardian_address,
            guardian_whatsapp=guardian_whatsapp,
            guardian_place=guardian_place,
            guardian_area=guardian_area,
            guardian_location=guardian_location,
            guardian_state=guardian_state,
            guardian_city=guardian_city,

            corres_address=corres_address,
            corres_mobile_no=corres_mobile_no,
            corres_whatsapp=corres_whatsapp,
            corres_place=corres_place,
            corres_area=corres_area,
            corres_location=corres_location,
            corres_state=corres_state,
            corres_city=corres_city,
            custid=user,
            school=a1
        )

        name1 = request.POST.get('name1')
        age1 = request.POST.get('age1')
        gender1 = request.POST.get('gender1')
        school1 = request.POST.get('school1')
        class1 = request.POST.get('class1')

        name2 = request.POST.get('name2')
        age2 = request.POST.get('age2')
        gender2 = request.POST.get('gender2')
        school2 = request.POST.get('school2')
        class2 = request.POST.get('class2')

        name3 = request.POST.get('name3')
        age3 = request.POST.get('age3')
        gender3 = request.POST.get('gender3')
        school3 = request.POST.get('school3')
        class3 = request.POST.get('class3')

        name4 = request.POST.get('name4')
        age4 = request.POST.get('age4')
        gender4 = request.POST.get('gender4')
        school4 = request.POST.get('school4')
        class4 = request.POST.get('class4')

        name5 = request.POST.get('name5')
        age5 = request.POST.get('age5')
        gender5 = request.POST.get('gender5')
        school5 = request.POST.get('school5')
        class5 = request.POST.get('class5')

        admission_form = request.POST.get('admission_form')
        admission_form_remarks = request.POST.get('admission_form_remarks')

        school_leaving_certificate = request.POST.get('school_leaving_certificate')
        school_leaving_certificate_remarks = request.POST.get('school_leaving_certificate_remarks')

        bonafide_certificate = request.POST.get('bonafide_certificate')
        bonafide_certificate_remarks = request.POST.get('bonafide_certificate_remarks')

        birth_certificate = request.POST.get('birth_certificate')
        birth_certificate_remarks = request.POST.get('birth_certificate_remarks')

        caste_certificate = request.POST.get('caste_certificate')
        caste_certificate_remarks = request.POST.get('caste_certificate_remarks')

        all_documents = request.POST.get('all_documents')
        all_documents_remarks = request.POST.get('all_documents_remarks')

        ration_card = request.POST.get('ration_card')
        ration_card_remarks = request.POST.get('ration_card_remarks')

        student_adhar_certificate = request.POST.get('student_adhar_certificate')
        student_adhar_certificate_remarks = request.POST.get('student_adhar_certificate_remarks')

        father_adhar_certificate = request.POST.get('father_adhar_certificate')
        father_adhar_certificate_remarks = request.POST.get('father_adhar_certificate_remarks')

        mother_adhar_certificate = request.POST.get('mother_adhar_certificate')
        mother_adhar_certificate_remarks = request.POST.get('mother_adhar_certificate_remarks')

        mn=SiblingDocumentSubmission(
            stdid=student,
            name1=name1,
            age1=age1,
            gender1=gender1,
            school1=school1,
            class1=class1,

            name2=name2,
            age2=age2,
            gender2=gender2,
            school2=school2,
            class2=class2,

            name3=name3,
            age3=age3,
            gender3=gender3,
            school3=school3,
            class3=class3,

            name4=name4,
            age4=age4,
            gender4=gender4,
            school4=school4,
            class4=class4,

            name5=name5,
            age5=age5,
            gender5=gender5,
            school5=school5,
            class5=class5,

            admission_form=admission_form,
            admission_form_remarks=admission_form_remarks,

            school_leaving_certificate=school_leaving_certificate,
            school_leaving_certificate_remarks=school_leaving_certificate_remarks,

            bonafide_certificate=bonafide_certificate,
            bonafide_certificate_remarks=bonafide_certificate_remarks,

            birth_certificate=birth_certificate,
            birth_certificate_remarks=birth_certificate_remarks,

            caste_certificate=caste_certificate,
            caste_certificate_remarks=caste_certificate_remarks,

            all_documents=all_documents,
            all_documents_remarks=all_documents_remarks,

            ration_card=ration_card,
            ration_card_remarks=ration_card_remarks,

            student_adhar_certificate=student_adhar_certificate,
            student_adhar_certificate_remarks=student_adhar_certificate_remarks,

            father_adhar_certificate=father_adhar_certificate,
            father_adhar_certificate_remarks=father_adhar_certificate_remarks,

            mother_adhar_certificate=mother_adhar_certificate,
            mother_adhar_certificate_remarks=mother_adhar_certificate_remarks,
            custid=user,
            school=a1
        )
        mn.save()



        
                
        transport_available = request.POST.get('transportAvailable')
        if transport_available == 'yes':
            bus_no = request.POST.get('busNo')
            driver_name = request.POST.get('driverName')
            mobile = request.POST.get('mobile')
            route = request.POST.get('route')
            stoppage = request.POST.get('stoppage')
            fee_id = request.POST.get('fee1')
            if fee_id:
                fee_obj = TransportFee.objects.filter(id=fee_id, school=a1).first()
            pick_up = request.POST.get('pickUp')
            drop_off = request.POST.get('dropOff')
            fee_category = request.POST.get('feeCategory')
            fee_type = request.POST.get('feeType')
        else:
            bus_no = ''
            driver_name = ''
            mobile = ''
            route = ''
            stoppage = ''
            fee_id = ''
            fee_obj = None
            pick_up = ''
            drop_off = ''
            fee_category = ''
            fee_type = ''

        
        # Save the data to the database
        transport_info = TransportInformation(
            stdid=student,
            transport_available=transport_available,
            bus_no=bus_no,
            driver_name=driver_name,
            mobile=mobile,
            route=route,
            stoppage=stoppage,
            fee1=fee_obj,
            pick_up=pick_up,
            drop_off=drop_off,
            fee_category=fee_category,
            fee_type=fee_type,
            custid=user,
            school=a1
        )
        transport_info.save()


        return redirect(student_list)

    return render(request, 'insert_student_admission.html',{'students':students,'next_admission_id':next_admission_id,'fees':fees,'bus_numbers': bus_numbers,'routes':routes,'a1':a1,'trans':trans})


def get_driver_details(request):
    bus_no = request.GET.get('bus_no')
    try:
        transport = Transport.objects.get(vechile_number=bus_no)
        data = {
            'driver_name': transport.driver.name if transport.driver else '',
            'mobile': transport.driver.phone if transport.driver else '',
            'route_id': transport.route.id if transport.route else '',
            'route_name': transport.route.name if transport.route else '',
            'start_point': transport.route.start_point if transport.route else '',
            'end_point': transport.route.end_point if transport.route else ''
        }
    except Transport.DoesNotExist:
        data = {
            'driver_name': '',
            'mobile': '',
            'route_id': '',
            'route_name': '',
            'start_point': '',
            'end_point': ''
        }

    return JsonResponse(data)




from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import io
import openpyxl

def student_list(request):
    # Student list functionality
    try:
        a1 = SchoolDetails.objects.get(custid=request.user)
    except SchoolDetails.DoesNotExist:
        messages.error(request, "School details not found!")
        return redirect('admin_dashboard')  # Redirect if school is not set up
    
    search_query = request.GET.get('search', '')
    page_number = request.GET.get('page', 1)

    # Filter student records based on the search query
    if search_query:
        students = studentadmission.objects.filter(
            Q(registrationno__icontains=search_query) | 
            Q(studentname__icontains=search_query) | 
            Q(classs__icontains=search_query)
        )
    else:
        students = studentadmission.objects.filter(school=a1)

    # Paginate the student records
    paginator = Paginator(students, 10)  # Show 10 records per page
    students_page = paginator.get_page(page_number)

    # Fetch related data
    education_details = {e.stdid_id: e for e in EducationDetail.objects.filter(school=a1)}
    previous_schools = {p.stdid_id: p for p in Previousschooling.objects.filter(school=a1)}
    family_details = {f.stdid_id: f for f in FamilyDetails.objects.filter(school=a1)}
    sibling_docs = {s.stdid_id: s for s in SiblingDocumentSubmission.objects.filter(school=a1)}
    transport_info = {t.stdid_id: t for t in TransportInformation.objects.filter(school=a1)}

    # Combine student data
    combined_data = [
        (
            student,
            education_details.get(student.id, None),
            previous_schools.get(student.id, None),
            family_details.get(student.id, None),
            sibling_docs.get(student.id, None),
            transport_info.get(student.id, None),
        )
        for student in students_page
    ]

    no_data_found = not students.exists()
    
    # Credentials functionality
    mn = Class.objects.all()
    credentials = StudentCredentials.objects.filter(school=a1)
    
    if request.method == 'POST':
        selected_classes = request.POST.getlist('class_select')
        file_format = request.POST.get('file_format')
        password = request.POST.get('password', '')
        
        class_credentials = StudentCredentials.objects.filter(
            studentid__classs__name__in=selected_classes,school=a1
        )
        
        if file_format == 'pdf':
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            elements = []
            
            data = [['Username', 'Email', 'Role', 'Student Name', 'Class']]
            for cred in class_credentials:
                data.append([
                    cred.username,
                    cred.email,
                    cred.role,
                    cred.studentid.studentname,
                    cred.studentid.classs.name
                ])
            
            table = Table(data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 14),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            elements.append(table)
            doc.build(elements)
            
            buffer.seek(0)
            response = HttpResponse(buffer, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="credentials.pdf"'
            return response
            
        elif file_format == 'excel':
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Student Credentials"
            
            headers = ['Username', 'Email', 'Role', 'Student Name', 'Class']
            ws.append(headers)
            
            for cred in class_credentials:
                ws.append([
                    cred.username,
                    cred.email,
                    cred.role,
                    cred.studentid.studentname,
                    cred.studentid.classs.name
                ])
            
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = f'attachment; filename="credentials.xlsx"'
            
            buffer = io.BytesIO()
            wb.save(buffer)
            buffer.seek(0)
            response.write(buffer.getvalue())
            return response

    context = {
        'combined_data': combined_data,
        'no_data_found': no_data_found,
        'search_query': search_query,
        'students_page': students_page,
        'credentials': credentials,
        'mn': mn,
        'a1':a1
    }
    return render(request, 'student_list1.html', context)


def login_list(request):
    try:
        a1 = SchoolDetails.objects.get(custid=request.user)
    except SchoolDetails.DoesNotExist:
        messages.error(request, "School details not found!")
        return redirect('admin_dashboard')  # Redirect if school is not set up
    search_query = request.GET.get('search', '')  # Get the search term from the URL parameters
    page_number = request.GET.get('page', 1)  # Get current page number from request

    # Filter student records based on the search query
    if search_query:
        students = studentadmission.objects.filter(
            Q(registrationno__icontains=search_query) | 
            Q(studentname__icontains=search_query) | 
            Q(classs__icontains=search_query)
        )
    else:
        students = studentadmission.objects.filter(school=a1)

    # Paginate the student records
    paginator = Paginator(students, 10)  # Show 10 records per page
    students_page = paginator.get_page(page_number)

    # Fetch related data based on student ID
    education_details = {e.stdid_id: e for e in EducationDetail.objects.filter(school=a1)}
    previous_schools = {p.stdid_id: p for p in Previousschooling.objects.filter(school=a1)}
    family_details = {f.stdid_id: f for f in FamilyDetails.objects.filter(school=a1)}
    sibling_docs = {s.stdid_id: s for s in SiblingDocumentSubmission.objects.filter(school=a1)}
    transport_info = {t.stdid_id: t for t in TransportInformation.objects.filter(school=a1)}

    # Combine data while handling missing values
    combined_data = [
        (
            student,
            education_details.get(student.id, None),
            previous_schools.get(student.id, None),
            family_details.get(student.id, None),
            sibling_docs.get(student.id, None),
            transport_info.get(student.id, None),
        )
        for student in students_page
    ]

    # Check if any student is found
    no_data_found = not students.exists()

    return render(request, "login_list1.html", {
        'combined_data': combined_data, 
        'no_data_found': no_data_found, 
        'search_query': search_query,
        'students_page': students_page,
        'a1':a1  
    })


def std_edit(request, id):
    try:
        ob = studentadmission.objects.get(id=id)
        ob1 = EducationDetail.objects.filter(stdid_id=id)
        
        # Handle missing Previousschooling record
        ob2 = Previousschooling.objects.filter(stdid_id=id).first()
        
        ob3 = FamilyDetails.objects.get(stdid_id=id)
        ob4 = SiblingDocumentSubmission.objects.get(stdid_id=id)
      

        # Fetch all class and section data
        class_list = Class.objects.all()
        section_list = Section.objects.filter(class_assigned=ob.classs)

    except studentadmission.DoesNotExist:
        raise Http404("Student not found")

    return render(
        request, 
        "update_std.html", 
        {
            'ob': ob, 
            'ob1': ob1, 
            'ob2': ob2, 
            'ob3': ob3, 
            'ob4': ob4, 
            
            'class_list': class_list,
            'section_list': section_list
        }
    )



def login_edit(request, id):
        try:
            a1 = SchoolDetails.objects.get(custid=request.user)
        except SchoolDetails.DoesNotExist:
            messages.error(request, "School details not found!")
            return redirect('admin_dashboard')
        
        ob = CustomUser.objects.get(id=id)
        ob1=studentadmission.objects.get(custid=id)
       
        return render(request, "login_update.html", {'ob': ob,'ob1':ob1,'a1':a1})




def update_login(request, id):
    user = get_object_or_404(CustomUser, id=id)
  
    student_credentials = StudentCredentials.objects.filter(user=user).first()

    if request.method == 'POST':
        username = request.POST.get('username', user.username)
        email = request.POST.get('email', user.email)
        password = request.POST.get('password', None)
        role = request.POST.get('role', user.role)

        if CustomUser.objects.filter(username=username).exclude(id=user.id).exists():
            return render(request, 'login_update.html', {'error': 'Username already exists', 'user': user})

        user.username = username
        user.email = email
        user.role = role
        
        if password: 
            user.password = make_password(password)
        
        user.save()

        if student_credentials:
            student_credentials.username = username
            student_credentials.email = email
            student_credentials.role = role
            
            if password:  
                student_credentials.password = password  

            student_credentials.save()

        return redirect('login_list')  

    return render(request, 'login_update.html', {'user': user})


def update_student(request, id):
    if request.method == 'POST':
        # Retrieve student admission data
        student = studentadmission.objects.get(id=id) 
        
        # Update student fields 
        student.enqno = request.POST.get('enqno')
        student.session = request.POST.get('session')
        student.registrationno = request.POST.get('registrationno')
        # Update ForeignKey fields with related object references
        # student.classs = get_object_or_404(Class, id=request.POST.get('classs'))
        # student.section = get_object_or_404(Section, id=request.POST.get('section'))
        student.srnno = request.POST.get('srnno')
        student.formno = request.POST.get('formno')
        student.studenttype = request.POST.get('studenttype')
        student.studentname = request.POST.get('studentname')
        student.gender = request.POST.get('gender')
        student.dateofbirth = request.POST.get('dateofbirth')
        student.aadharno = request.POST.get('aadharno')
        student.house = request.POST.get('house')
        student.stream = request.POST.get('stream')
        student.emil = request.POST.get('emil')
        student.previousyearattendance = request.POST.get('previousyearattendance')
        student.mothertongue = request.POST.get('mothertongue')
        student.adoptedchild = request.POST.get('adoptedchild')
        student.minority = request.POST.get('minority')
        student.specify = request.POST.get('specify')
        student.nationality = request.POST.get('nationality')
        student.mediumofinstruction = request.POST.get('mediumofinstruction')
        student.castecategory = request.POST.get('castecategory')
        student.optionalsubject = request.POST.get('optionalsubject')
        student.offeredsubject = request.POST.get('offeredsubject')
        student.penno = request.POST.get('penno')
        student.bloodgroup = request.POST.get('bloodgroup')
        student.leftvision = request.POST.get('leftvision')
        student.rightvision = request.POST.get('rightvision')
        student.weight = request.POST.get('weight')
        student.height = request.POST.get('height')
        student.weight1 = request.POST.get('weight1')
        student.height1 = request.POST.get('height1')
        student.disability = request.POST.get('disability')
        student.sportsactivity = request.POST.get('sportsactivity')
        student.admissiondate = request.POST.get('admissiondate')
        student.bankname = request.POST.get('bankname')
        student.branchname = request.POST.get('branchname')
        student.accountno = request.POST.get('accountno')
        student.ifsccode = request.POST.get('ifsccode')
        student.profile_photo = request.FILES.get('profile_photo')


        student.save()  # Save updated student

        # Update Education Details
        edu_detail, created = EducationDetail.objects.get_or_create(stdid=student)
    
        edu_detail.qualificationf1 = request.POST.get('qualificationf1')
        edu_detail.specializationf1 = request.POST.get('specializationf1')
        edu_detail.institute_namef1 = request.POST.get('institute_namef1')
        edu_detail.statef1 = request.POST.get('statef1')
        edu_detail.cityf1 = request.POST.get('cityf1')
        
        edu_detail.qualificationf2 = request.POST.get('qualificationf2')
        edu_detail.specializationf2 = request.POST.get('specializationf2')
        edu_detail.institute_namef2 = request.POST.get('institute_namef2')
        edu_detail.statef2 = request.POST.get('statef2')
        edu_detail.cityf2 = request.POST.get('cityf2')
        
        edu_detail.qualificationf3 = request.POST.get('qualificationf3')
        edu_detail.specializationf3 = request.POST.get('specializationf3')
        edu_detail.institute_namef3 = request.POST.get('institute_namef3')
        edu_detail.statef3 = request.POST.get('statef3')
        edu_detail.cityf3 = request.POST.get('cityf3')
        
        edu_detail.qualificationf4 = request.POST.get('qualificationf4')
        edu_detail.specializationf4 = request.POST.get('specializationf4')
        edu_detail.institute_namef4 = request.POST.get('institute_namef4')
        edu_detail.statef4 = request.POST.get('statef4')
        edu_detail.cityf4 = request.POST.get('cityf4')
        
        edu_detail.qualificationf5 = request.POST.get('qualificationf5')
        edu_detail.specializationf5 = request.POST.get('specializationf5')
        edu_detail.institute_namef5 = request.POST.get('institute_namef5')
        edu_detail.statef5 = request.POST.get('statef5')
        edu_detail.cityf5 = request.POST.get('cityf5')
        
        edu_detail.qualificationm1 = request.POST.get('qualificationm1')
        edu_detail.specializationm1 = request.POST.get('specializationm1')
        edu_detail.institute_namem1 = request.POST.get('institute_namem1')
        edu_detail.statem1 = request.POST.get('statem1')
        edu_detail.citym1 = request.POST.get('citym1')
        
        edu_detail.qualificationm2 = request.POST.get('qualificationm2')
        edu_detail.specializationm2 = request.POST.get('specializationm2')
        edu_detail.institute_namem2 = request.POST.get('institute_namem2')
        edu_detail.statem2 = request.POST.get('statem2')
        edu_detail.citym2 = request.POST.get('citym2')
        
        edu_detail.qualificationm3 = request.POST.get('qualificationm3')
        edu_detail.specializationm3 = request.POST.get('specializationm3')
        edu_detail.institute_namem3 = request.POST.get('institute_namem3')
        edu_detail.statem3 = request.POST.get('statem3')
        edu_detail.citym3 = request.POST.get('citym3')
        
        edu_detail.qualificationm4 = request.POST.get('qualificationm4')
        edu_detail.specializationm4 = request.POST.get('specializationm4')
        edu_detail.institute_namem4 = request.POST.get('institute_namem4')
        edu_detail.statem4 = request.POST.get('statem4')
        edu_detail.citym4 = request.POST.get('citym4')
        
        edu_detail.qualificationm5 = request.POST.get('qualificationm5')
        edu_detail.specializationm5 = request.POST.get('specializationm5')
        edu_detail.institute_namem5 = request.POST.get('institute_namem5')
        edu_detail.statem5 = request.POST.get('statem5')
        edu_detail.citym5 = request.POST.get('citym5')
        
        edu_detail.qualificationg1 = request.POST.get('qualificationg1')
        edu_detail.specializationg1 = request.POST.get('specializationg1')
        edu_detail.institute_nameg1 = request.POST.get('institute_nameg1')
        edu_detail.stateg1 = request.POST.get('stateg1')
        edu_detail.cityg1 = request.POST.get('cityg1')
        
        edu_detail.qualificationg2 = request.POST.get('qualificationg2')
        edu_detail.specializationg2 = request.POST.get('specializationg2')
        edu_detail.institute_nameg2 = request.POST.get('institute_nameg2')
        edu_detail.stateg2 = request.POST.get('stateg2')
        edu_detail.cityg2 = request.POST.get('cityg2')
        
        edu_detail.qualificationg3 = request.POST.get('qualificationg3')
        edu_detail.specializationg3 = request.POST.get('specializationg3')
        edu_detail.institute_nameg3 = request.POST.get('institute_nameg3')
        edu_detail.stateg3 = request.POST.get('stateg3')
        edu_detail.cityg3 = request.POST.get('cityg3')
        
        edu_detail.qualificationg4 = request.POST.get('qualificationg4')
        edu_detail.specializationg4 = request.POST.get('specializationg4')
        edu_detail.institute_nameg4 = request.POST.get('institute_nameg4')
        edu_detail.stateg4 = request.POST.get('stateg4')
        edu_detail.cityg4 = request.POST.get('cityg4')
        
        edu_detail.qualificationg5 = request.POST.get('qualificationg5')
        edu_detail.specializationg5 = request.POST.get('specializationg5')
        edu_detail.institute_nameg5 = request.POST.get('institute_nameg5')
        edu_detail.stateg5 = request.POST.get('stateg5')
        edu_detail.cityg5 = request.POST.get('cityg5')
        
        edu_detail.save()

        

        # Update Previous Schooling Details
        school_names = request.POST.getlist('schoolnameandaddress[]')
        class_names = request.POST.getlist('classname[]')
        sessions = request.POST.getlist('session[]')
        curriculums = request.POST.getlist('curriculum[]')
        subjects = request.POST.getlist('subjects[]')

        for school_name, class_name, session, curriculum, subject in zip(
            school_names, class_names, sessions, curriculums, subjects
        ):
            if school_name:
                prev_school, created = Previousschooling.objects.get_or_create(stdid=student)
                prev_school.schoolnameandaddress = school_name
                prev_school.classname = class_name
                prev_school.session = session
                prev_school.curriculum = curriculum
                prev_school.subjects = subject
                prev_school.save()

        # Update Family Details
        family, created = FamilyDetails.objects.get_or_create(stdid=student)
        family.father_name = request.POST.get('father_name')
        family.father_email = request.POST.get('father_email')
        family.father_nationality = request.POST.get('father_nationality')
        family.father_occupation = request.POST.get('father_occupation')
        family.father_department = request.POST.get('father_department')
        family.father_designation = request.POST.get('father_designation')
        family.father_name_of_office = request.POST.get('father_name_of_office')
        family.father_office_address = request.POST.get('father_office_address')
        family.father_office_contact_no = request.POST.get('father_office_contact_no')
        family.father_aadhar_no = request.POST.get('father_aadhar_no')
        family.father_pan_no = request.POST.get('father_pan_no')
        family.father_annual_income = request.POST.get('father_annual_income')
        family.father_mobile = request.POST.get('father_mobile')
        family.father_mobile2 = request.POST.get('father_mobile2')
        family.father_religion = request.POST.get('father_religion')
        family.father_caste = request.POST.get('father_caste')
        family.father_marital_status = request.POST.get('father_marital_status')

        family.mother_name = request.POST.get('mother_name')
        family.mother_email = request.POST.get('mother_email')
        family.mother_nationality = request.POST.get('mother_nationality')
        family.mother_occupation = request.POST.get('mother_occupation')
        family.mother_department = request.POST.get('mother_department')
        family.mother_designation = request.POST.get('mother_designation')
        family.mother_name_of_office = request.POST.get('mother_name_of_office')
        family.mother_office_address = request.POST.get('mother_office_address')
        family.mother_office_contact_no = request.POST.get('mother_office_contact_no')
        family.mother_aadhar_no = request.POST.get('mother_aadhar_no')
        family.mother_pan_no = request.POST.get('mother_pan_no')
        family.mother_annual_income = request.POST.get('mother_annual_income')
        family.mother_mobile = request.POST.get('mother_mobile')
        family.mother_mobile2 = request.POST.get('mother_mobile2')
        family.mother_religion = request.POST.get('mother_religion')
        family.mother_caste = request.POST.get('mother_caste')
        family.mother_marital_status = request.POST.get('mother_marital_status')

        family.guardian_name = request.POST.get('guardian_name')
        family.guardian_email = request.POST.get('guardian_email')
        family.guardian_nationality = request.POST.get('guardian_nationality')
        family.guardian_occupation = request.POST.get('guardian_occupation')
        family.guardian_department = request.POST.get('guardian_department')
        family.guardian_designation = request.POST.get('guardian_designation')
        family.guardian_name_of_office = request.POST.get('guardian_name_of_office')
        family.guardian_office_address = request.POST.get('guardian_office_address')
        family.guardian_office_contact_no = request.POST.get('guardian_office_contact_no')
        family.guardian_aadhar_no = request.POST.get('guardian_aadhar_no')
        family.guardian_pan_no = request.POST.get('guardian_pan_no')
        family.guardian_annual_income = request.POST.get('guardian_annual_income')
        family.guardian_mobile = request.POST.get('guardian_mobile')
        family.guardian_mobile2 = request.POST.get('guardian_mobile2')
        family.guardian_religion = request.POST.get('guardian_religion')
        family.guardian_caste = request.POST.get('guardian_caste')
        family.guardian_marital_status = request.POST.get('guardian_marital_status')
        family.guardian_relation = request.POST.get('guardian_relation')
        family.guardian_address = request.POST.get('guardian_address')
        family.guardian_whatsapp = request.POST.get('guardian_whatsapp')
        family.guardian_place = request.POST.get('guardian_place')
        family.guardian_area = request.POST.get('guardian_area')
        family.guardian_location = request.POST.get('guardian_location')
        family.guardian_state = request.POST.get('guardian_state')
        family.guardian_city = request.POST.get('guardian_city')

        family.corres_address = request.POST.get('corres_address')
        family.corres_mobile_no = request.POST.get('corres_mobile_no')
        family.corres_whatsapp = request.POST.get('corres_whatsapp')
        family.corres_place = request.POST.get('corres_place')
        family.corres_area = request.POST.get('corres_area')
        family.corres_location = request.POST.get('corres_location')
        family.corres_state = request.POST.get('corres_state')
        family.corres_city = request.POST.get('corres_city')

        family.save()

        # Update Document Submission
        doc, created = SiblingDocumentSubmission.objects.get_or_create(stdid=student)
        doc.name1 = request.POST.get('name1')
        doc.age1 = request.POST.get('age1')
        doc.gender1 = request.POST.get('gender1')
        doc.school1 = request.POST.get('school1')
        doc.class1 = request.POST.get('class1')

        doc.name2 = request.POST.get('name2')
        doc.age2 = request.POST.get('age2')
        doc.gender2 = request.POST.get('gender2')
        doc.school2 = request.POST.get('school2')
        doc.class2 = request.POST.get('class2')

        doc.name3 = request.POST.get('name3')
        doc.age3 = request.POST.get('age3')
        doc.gender3 = request.POST.get('gender3')
        doc.school3 = request.POST.get('school3')
        doc.class3 = request.POST.get('class3')

        doc.name4 = request.POST.get('name4')
        doc.age4 = request.POST.get('age4')
        doc.gender4 = request.POST.get('gender4')
        doc.school4 = request.POST.get('school4')
        doc.class4 = request.POST.get('class4')

        doc.name5 = request.POST.get('name5')
        doc.age5 = request.POST.get('age5')
        doc.gender5 = request.POST.get('gender5')
        doc.school5 = request.POST.get('school5')
        doc.class5 = request.POST.get('class5')

        doc.admission_form = request.POST.get('admission_form')
        doc.admission_form_remarks = request.POST.get('admission_form_remarks')
        doc.school_leaving_certificate = request.POST.get('school_leaving_certificate')
        doc.school_leaving_certificate_remarks = request.POST.get('school_leaving_certificate_remarks')
        doc.bonafide_certificate = request.POST.get('bonafide_certificate')
        doc.bonafide_certificate_remarks = request.POST.get('bonafide_certificate_remarks')
        doc.birth_certificate = request.POST.get('birth_certificate')
        doc.birth_certificate_remarks = request.POST.get('birth_certificate_remarks')
        doc.caste_certificate = request.POST.get('caste_certificate')
        doc.caste_certificate_remarks = request.POST.get('caste_certificate_remarks')
        doc.all_documents = request.POST.get('all_documents')
        doc.all_documents_remarks = request.POST.get('all_documents_remarks')
        doc.ration_card = request.POST.get('ration_card')
        doc.ration_card_remarks = request.POST.get('ration_card_remarks')
        doc.student_adhar_certificate = request.POST.get('student_adhar_certificate')
        doc.student_adhar_certificate_remarks = request.POST.get('student_adhar_certificate_remarks')
        doc.father_adhar_certificate = request.POST.get('father_adhar_certificate')
        doc.father_adhar_certificate_remarks = request.POST.get('father_adhar_certificate_remarks')
        doc.mother_adhar_certificate = request.POST.get('mother_adhar_certificate')
        doc.mother_adhar_certificate_remarks = request.POST.get('mother_adhar_certificate_remarks')
        doc.save()

        return JsonResponse({'message': 'Student details updated successfully'})

    return render(request,"update_std.html")


def std_delete(request,id):
    ob=studentadmission.objects.get(id=id)
    ob1=EducationDetail.objects.filter(stdid=id)
    ob2=Previousschooling.objects.filter(stdid=id)
    ob3=FamilyDetails.objects.filter(stdid=id)
    ob4=SiblingDocumentSubmission.objects.filter(stdid=id)
    ob5=TransportInformation.objects.filter(stdid=id)
    ob.delete()
    ob1.delete()
    ob2.delete()
    ob3.delete()
    ob4.delete()
    ob5.delete()
    return redirect('/student_list/')    



from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
import random

# Store OTP temporarily (for production, use session or cache)
stored_otp = {}

def user_login(request):
    context = {}

    if request.method == 'POST':
        if 'username' in request.POST:
            # Dashboard login with Django auth
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('dashboard')  # or wherever you want to redirect
            else:
                messages.error(request, "Invalid credentials!")
                context['active_form'] = 'dashboard'

        elif 'send_otp' in request.POST:
            email_entered = request.POST['email']
            valid_email = 'surendraderangula22@gmail.com'  # Change as needed

            if email_entered != valid_email:
                messages.error(request, "Invalid email! Please use the correct one.")
                context['active_form'] = 'registration'
            else:
                otp = str(random.randint(100000, 999999))
                stored_otp['otp'] = otp
                stored_otp['email'] = email_entered

                send_mail(
                    'Your OTP Code',
                    f'Your OTP is: {otp}',
                    'admin@example.com',
                    [email_entered],
                    fail_silently=False,
                )
                messages.success(request, f"OTP sent to {email_entered}.")
                context['email_sent'] = True
                context['email'] = email_entered
                context['active_form'] = 'registration'

        elif 'verify_otp' in request.POST:
            otp_entered = request.POST['otp']
            if stored_otp.get('otp') == otp_entered:
                messages.success(request, 'Login successful!')
                return redirect('add_school_details')  # Change to your school dashboard view
            else:
                messages.error(request, 'Invalid OTP!')
                context['email_sent'] = True
                context['email'] = stored_otp.get('email')
                context['active_form'] = 'registration'

    # Default to dashboard form on GET
    if 'active_form' not in context:
        context['active_form'] = request.GET.get('show', 'dashboard')

    return render(request, 'login.html', context)


def user_logout(request):
    logout(request)
    return redirect('user_login')   


from django.shortcuts import render
from django.utils.timezone import now
from django.db.models import Count
from datetime import datetime
import calendar
from .models import Attendance
from calendar import monthrange



def dashboard(request):
  

    if not request.user.is_authenticated:
        return redirect('login')

    try:
        i = studentadmission.objects.get(custid=request.user)
    except studentadmission.DoesNotExist:
        i = None  
    try:
        n = TransportInformation.objects.get(custid=request.user)
    except TransportInformation.DoesNotExist:
        n = None

    try:
        j = EducationDetail.objects.get(custid=request.user)
    except EducationDetail.DoesNotExist:
        j = None     

    try:
        k = Previousschooling.objects.get(custid=request.user)
    except Previousschooling.DoesNotExist:
        k = None    

    try:
        l = FamilyDetails.objects.get(custid=request.user)
    except FamilyDetails.DoesNotExist:
        l = None 

    try:
        m = SiblingDocumentSubmission.objects.get(custid=request.user)
    except SiblingDocumentSubmission.DoesNotExist:
        m = None    

    try:
        o = student_fee_Amount.objects.get(custid=request.user)
    except student_fee_Amount.DoesNotExist:
        o = None   


    # Initialize default counts
    admin_present_count = 0
    admin_absent_count = 0
    admin_total = 0

    if request.method == 'POST' and request.POST.get('class_id') and request.POST.get('section_id'):
        class_id = request.POST.get('class_id')
        section_id = request.POST.get('section_id')

        students = studentadmission.objects.filter(
            student_class_id=class_id,
            section_id=section_id,
            school=request.user.schooldetails
        )
        admin_total = students.count()
        presdmin_present_countent = Attendance.objects.filter(student__in=students, date=today, status='Present').count()
        admin_total = Attendance.objects.filter(student__in=students, date=today, status='Absent').count()


    try:
        a1 = SchoolDetails.objects.get(custid=request.user)
    except SchoolDetails.DoesNotExist:
        a1 = None 
    std = studentadmission.objects.filter(school=a1).count()
    std111 = studentadmission.objects.filter(school=a1)
    std1 = studentadmission.objects.filter(school=a1, admissiondate=date.today()).count()
    teach=Teacher.objects.filter(school=a1).count()
    clas=Class.objects.filter(school=a1).count()
    classes=Class.objects.filter(school=a1)
    sections = Section.objects.filter(school=a1)
    sec=Section.objects.filter(school=a1).count()
    total_fee = student_fee_Amount.objects.aggregate(total=models.Sum('total_amount'))['total'] or 0
    amount = StudentPayment.objects.aggregate(total=Sum('amount1'))['total'] or 0
    balance_amount = total_fee - amount

    today = timezone.now().date()
    birthday_students = studentadmission.objects.filter(
        dateofbirth__day=today.day,
        dateofbirth__month=today.month,school=a1
    )
    birthday_teachers = Teacher.objects.filter(
        date_of_birth__day=today.day,
        date_of_birth__month=today.month,school=a1
    )
    student_custom_users = CustomUser.objects.filter(
    role='student',
    id__in=studentadmission.objects.filter(school=a1).values_list('custid', flat=True)
    )

    student_leave_requests = LeaveRequest.objects.filter(
        student__in=student_custom_users,
        created_at__date=today
    )

    teacher_custom_users = CustomUser.objects.filter(
    role='teacher',
    id__in=Teacher.objects.filter(school=a1).values_list('custid', flat=True)
    )

    teacher_leave_requests = LeaveRequest.objects.filter(
        student__in=teacher_custom_users,
        created_at__date=today
    )
    try:
        fm = Teacher.objects.get(custid=request.user)
    except Teacher.DoesNotExist:
        fm = None 

    if fm is not None:
        try:
            headings = teacherdashboardheading.objects.filter(school=fm.school).prefetch_related('teachersubmenu_set')
        except teacherdashboardheading.DoesNotExist:
            headings = None

    else:
        headings = None
    

    user = request.user
    today = timezone.now().date()

    # Try to get the teacher, return None if not found
    teacher = Teacher.objects.filter(custid=user).first()

    # If teacher is not found, set default values or handle the case
    if teacher:
        # Safe to access related fields now
        assigned_class = teacher.assigned_classes1.first() if teacher.assigned_classes1.exists() else None
        assigned_section = teacher.assigned_sections1.first() if teacher.assigned_sections1.exists() else None

        total_students = 0
        present_count = 0
        absent_count = 0
        class_name = ''
        section_name = ''

        if assigned_class and assigned_section:
            # Get the students assigned to this class and section
            students = studentadmission.objects.filter(
                classs=assigned_class,
                section=assigned_section,
                school=teacher.school
            )
            total_students = students.count()
            class_name = assigned_class.name
            section_name = assigned_section.name

            # Attendance today
            attendance_today = Attendance.objects.filter(
                student__in=students,
                date=today
            )
            present_count = attendance_today.filter(status='Present').count()
            absent_count = attendance_today.filter(status='Absent').count()
    else:
        # Handle the case where the teacher is not found, e.g., set defaults or display a message
        assigned_class = assigned_section = None
        total_students = present_count = absent_count = 0
        class_name = section_name = "N/A"


    leave_requests = TeacherLeaveRequest.objects.all().order_by('-created_at')
    
    is_class_teacher = False

    if teacher and teacher.assigned_classes1.exists() and teacher.assigned_sections1.exists():
        is_class_teacher = True
        # Fetch students in any of the assigned classes and sections
        students = studentadmission.objects.filter(
            classs__in=teacher.assigned_classes1.all(),
            section__in=teacher.assigned_sections1.all(),
            school=teacher.school
        )

        birthday_students = studentadmission.objects.filter(
            classs__in=teacher.assigned_classes1.all(),
            section__in=teacher.assigned_sections1.all(),
            dateofbirth__day=today.day,
            dateofbirth__month=today.month,
            school=teacher.school
        )    

        user_ids = students.values_list('custid_id', flat=True)
        leave_requests = LeaveRequest.objects.filter(student_id__in=user_ids).order_by('-created_at')


        # Today's attendance records
        attendance_records = Attendance.objects.filter(
            student__in=students,
            date=today
        )

        attendance_summary = attendance_records.values('status').annotate(count=Count('id'))
        for record in attendance_summary:
            if record['status'] == 'Present':
                present_count = record['count']
            elif record['status'] == 'Absent':
                absent_count = record['count']


# -----------------------------------------  Student Dashboard   -----------------------------------------------------------


        
    day_labels = []
    status_list = []
    numeric_data = []
    color_data = []
    student_present_count = 0
    student_absent_count = 0

    user = request.user


    try:
        student = studentadmission.objects.get(custid=user)
    except studentadmission.DoesNotExist:
        student = None
    

    today = timezone.now()
    year = today.year
    month = today.month
    num_days = monthrange(year, month)[1]

    attendance_data = Attendance.objects.filter(
        student=student,
        date__year=year,
        date__month=month
    )

    daily_status = {record.date.day: record.status for record in attendance_data}

    for day in range(1, num_days + 1):
        day_labels.append(day)
        status = daily_status.get(day, 'No Data')
        status_list.append(status)

        if status == 'Present':
            numeric_data.append(1)
            color_data.append('#4CAF50')
        elif status == 'Absent':
            numeric_data.append(0)
            color_data.append('#F44336')
        else:
            numeric_data.append(None)  # Chart.js can handle null
            color_data.append('#cccccc')

    student_present_count = status_list.count('Present')
    student_absent_count = status_list.count('Absent')


    

    student = request.user
    admission = studentadmission.objects.filter(custid=student).first()  # Assuming one-to-one

    # Fetch academic fee data
    fee_data = student_fee_Amount.objects.filter(stdid=admission).first()

    # Total academic fee
    total_fee = fee_data.original_amount if fee_data else 0

    # Transport fee (if any)
    transport_fee = 0
    transport = TransportInformation.objects.filter(stdid=admission).first()
    if transport and transport.fee1:
        transport_fee = transport.fee1.amount

    # Total of all payments made
    payments = StudentPayment.objects.filter(admission_id=admission)
    paid_amount = payments.aggregate(total=Sum('amount1'))['total'] or 0

    # Final total including transport
    grand_total = total_fee + transport_fee
    balance = grand_total - paid_amount

    pie_labels = ['Paid Amount', 'Balance Amount']
    pie_values = [paid_amount, balance]

    # Bar chart can still show part1/part2/part3 if you want
    bar_labels = ['Term 1', 'Term 2', 'Term 3']
    bar_values = [fee_data.part1, fee_data.part2, fee_data.part3] if fee_data else [0, 0, 0]



# --------------------------------------------------------------------------------------------------------



    context = {
        'user': request.user,
        'i' : i,
        'j' : j,
        'k' : k,
        'l' : l,
        'm' : m,
        'n' : n,
        'o' : o,
        'a1':a1,
        'fm':fm,
        'headings':headings,
        'std':std,'std111':std111,'teach':teach,'clas':clas,'sec':sec,'total_fee':total_fee,'amount':amount,'balance_amount':balance_amount,'std1':std1,
        'total_students': total_students,
        'class_name': class_name,
        'section_name': section_name,
        'students': birthday_students,'birthday_teachers':birthday_teachers,'student_leave_requests': student_leave_requests,
        'teacher_leave_requests': teacher_leave_requests,
        'leave_requests': leave_requests,
        'is_class_teacher': is_class_teacher,
        'birthday_students':birthday_students,
        'leave_requests':leave_requests,
        'present_count': present_count,
        'absent_count': absent_count,
        'total_count': present_count + absent_count,
        'admin_present_count':admin_present_count,
        'admin_absent_count':admin_absent_count,
        'admin_total':admin_total,
        'classes':classes,
        'sections':sections,
        'day_labels': json.dumps(day_labels),
        'numeric_data': json.dumps(numeric_data),
        'color_data': json.dumps(color_data),
        'student_present_count': student_present_count,
        'student_absent_count': student_absent_count,
        'combined_attendance': list(zip(day_labels, status_list)),
        'num_days': num_days,
        'pie_labels': pie_labels,
        'pie_values': pie_values,
        'bar_labels': bar_labels,
        'bar_values': bar_values,
        'total_fee': grand_total,
        'paid_amount': paid_amount,
        'balance': balance,
        
      
    }

    if request.user.role == 'admin':
        return render(request, 'admin_base.html', context)
    elif request.user.role == 'teacher':
        return render(request, 'teacher_base.html', context)
    elif request.user.role == 'accountant':
        return render(request, 'accountant_dashboard.html', context)
    elif request.user.role == 'student':
        return render(request, 'student_base.html', context)
    elif request.user.role == 'non_teaching_staff':
        return render(request, 'non_teaching_staff_dashboard.html', context)


    return redirect('login')  

from decimal import Decimal, ROUND_HALF_UP
def student_profile(request, id):
    try:
        a1 = SchoolDetails.objects.get(custid=request.user)
    except SchoolDetails.DoesNotExist:
        messages.error(request, "School details not found!")
        return redirect('admin_dashboard')
    try:
        ob = studentadmission.objects.get(id=id)

    except studentadmission.DoesNotExist:
        raise Http404("Student not found")
    
    try:
        j = EducationDetail.objects.get(stdid=id)
    except EducationDetail.DoesNotExist:
        j = None     

    try:
        k = Previousschooling.objects.get(stdid=id)
    except Previousschooling.DoesNotExist:
        k = None    

    try:
        l = FamilyDetails.objects.get(stdid=id)
    except FamilyDetails.DoesNotExist:
        l = None 

    try:
        i = studentadmission.objects.get(id=id)
    except studentadmission.DoesNotExist:
        i = None
    try:
        o = student_fee_Amount.objects.get(stdid=id) 
    except student_fee_Amount.DoesNotExist:
        o = None
    
    try:
        pj = Attendance.objects.filter(student=id) 
    except Attendance.DoesNotExist:
        pj = None

    ob5 = get_object_or_404(TransportInformation, stdid=id)

    m = get_object_or_404(SiblingDocumentSubmission, stdid=id)

    trans = TransportFee.objects.filter(school=a1)

    fee_amount = ob5.fee1.fee if ob5.fee1 else Decimal('0.00')

    # Divide into 3 equal parts and round to 2 decimal places
    part = (fee_amount / 3).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    bus_numbers = Transport.objects.filter(school=a1).values_list('vechile_number', flat=True).distinct()
    routes = Route.objects.filter(school=a1)

    

    # Fetch classes and exams
    exams = exam.objects.filter(school=a1)

    # Initialize variables
    students = []
    results = []
    selected_exam = None

    # Initialize exam_id outside POST block
    exam_id = None

    if request.method == 'POST':
        exam_id = request.POST.get('exam_id')

        selected_exam = exam_id

        if exam_id:
            # Fetch students based on the selected filters
            students = studentadmission.objects.filter(school=a1)
            results = StudentMarks1.objects.filter(student__in=students, exam_id=exam_id)

    # Fetch the exam object for the selected exam_id
    exam_obj = get_object_or_404(exam, id=exam_id) if exam_id else None

    report_data = []
    
    # Loop through each student to gather their report card data
    for student in students:
        total_obtained = 0
        total_max_marks = 0

        # Fetch all marks for the student in the selected exam
        marks = StudentMarks1.objects.filter(student=id, exam=exam_obj).select_related('subject')

        # Fetch extra subject marks
        extra_subjects = ExtraSubjectMarks.objects.filter(student=id, exam=exam_obj)

        # Fetch individual marks from SubjectMarksDetail
        marks_details = SubjectMarksDetail.objects.filter(student=id, exam=exam_obj).select_related('subject')

        # Retrieve Co-Scholastic grading scale
        co_scholastic_grades = CoScholasticGrade.objects.all()

        # Retrieve discipline grade for the student and exam
        discipline_grade = DisciplineGrade.objects.filter(student=id, exam=exam_obj).first()

        # Retrieve remarks
        remark = Remark.objects.filter(student=id, exam=exam_obj).first()

        # Retrieve signature and report date
        signature = ReportCardSignature.objects.filter(student=id, exam=exam_obj).first()

        # Organize marks into individual categories
        student_report_data = []
        for index, mark in enumerate(marks_details, start=1):
            total = mark.total
            total_obtained += total
            total_max_marks += 100

            # Grade Calculation
            if total >= 91:
                grade = "A1"
            elif total >= 81:
                grade = "A2"
            elif total >= 71:
                grade = "B1"
            elif total >= 61:
                grade = "B2"
            elif total >= 51:
                grade = "C1"
            elif total >= 41:
                grade = "C2"
            else:
                grade = "D"

            student_report_data.append({
                'sno': index,
                'subject': mark.subject.name,
                'pa': mark.pa,
                'se': mark.se,
                'ma': mark.ma,
                'nb': mark.nb,
                'term': mark.term,
                'total': mark.total,
                'grade': grade,
            })

        # Calculate overall percentage
        percentage = round((total_obtained / total_max_marks) * 100, 2) if total_max_marks > 0 else 0

        # Filter photo based on user school, class, section, and exam
        class_photo = ClassPhoto1.objects.filter(
            school=a1,
            exam=exam_obj
        ).first()

        # Append each student's report data to the overall report
        report_data.append({
            'student': student,
            'report_data': student_report_data,
            'total_obtained': total_obtained,
            'total_max_marks': total_max_marks,
            'percentage': percentage,
            'extra_subjects': extra_subjects,
            'co_scholastic_grades': co_scholastic_grades,
            'discipline_grade': discipline_grade,
            'remark': remark,
            'signature': signature,
            'class_photo': class_photo,
            'marks' : marks,
            
        })
    

    total_paid = 0
    paid1, paid2, paid3 = 0, 0, 0
    balance1, balance2, balance3 = 0, 0, 0

    if o:  
        payments = StudentPayment.objects.filter(custid=request.user).aggregate(total_paid=Sum('amount1'))
        total_paid = payments['total_paid'] or 0  
        
       
        balance1, balance2, balance3 = o.part1+part, o.part2+part, o.part3+part
        
       
        remaining_amount = total_paid
        if remaining_amount > 0:
            if remaining_amount >= o.part1:
                paid1 = o.part1
                remaining_amount -= o.part1
            else:
                paid1 = remaining_amount
                remaining_amount = 0

            if remaining_amount >= o.part2:
                paid2 = o.part2
                remaining_amount -= o.part2
            else:
                paid2 = remaining_amount
                remaining_amount = 0

            if remaining_amount >= o.part3:
                paid3 = o.part3
                remaining_amount -= o.part3
            else:
                paid3 = remaining_amount
                remaining_amount = 0
        
        # Calculate balance for each part
        balance1 = (o.part1+part) - paid1
        balance2 = (o.part2+part) - paid2
        balance3 = (o.part3+part) - paid3

    return render(
        request, 
        "student_profile.html", {
            'ob': ob, 
            'j' : j,
            'k' : k,
            'l' : l,
            
            'o': o,
        'total_paid': total_paid,
        'paid1': paid1,
        'paid2': paid2,
        'paid3': paid3,
        'balance1': balance1,
        'balance2': balance2,
        'balance3': balance3,
        'total_balance': balance1 + balance2 + balance3,
        'i':i,
        'pj':pj,
        'a1':a1,
        'ob5':ob5,
        'm' : m,
        'classes': classes,
        'exams': exams,
        'students': students,
        'results': results,
        'selected_exam': selected_exam,
        'report_data': report_data,  # Pass the report data for each student
        'a1':a1,
        'trans':trans,
        'part1': part,
        'part2': part,
        'part3': fee_amount - (part * 2),
        'bus_numbers':bus_numbers,
        'routes':routes,
        }
    )



def update_student_profile(request, id):
    if request.method == 'POST':
        try:
            trans = get_object_or_404(TransportInformation, stdid=id)

            trans.transport_available = request.POST.get('transport_available')
            trans.bus_no = request.POST.get('bus_no')
            trans.driver_name = request.POST.get('driver_name')
            trans.mobile = request.POST.get('mobile')
            trans.route = request.POST.get('route')
            trans.stoppage = request.POST.get('stoppage')
            
            fee_id = request.POST.get('fee1')
            if fee_id:
                trans.fee1 = TransportFee.objects.get(id=fee_id)
            else:
                trans.fee1 = None

            trans.pick_up = request.POST.get('pick_up')
            trans.drop_off = request.POST.get('drop_off')
            trans.fee_category = request.POST.get('fee_category')
            trans.fee_type = request.POST.get('fee_type')

            trans.save()
            return JsonResponse({'message': 'Student transport details updated successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return render(request, "student_profile.html")


def update_student_profile1(request, id):
    

    if request.method == 'POST':
        # Update Document Submission
        doc  = get_object_or_404(SiblingDocumentSubmission, stdid=id)
        doc.name1 = request.POST.get('name1')
        doc.age1 = request.POST.get('age1')
        doc.gender1 = request.POST.get('gender1')
        doc.school1 = request.POST.get('school1')
        doc.class1 = request.POST.get('class1')

        doc.name2 = request.POST.get('name2')
        doc.age2 = request.POST.get('age2')
        doc.gender2 = request.POST.get('gender2')
        doc.school2 = request.POST.get('school2')
        doc.class2 = request.POST.get('class2')

        doc.name3 = request.POST.get('name3')
        doc.age3 = request.POST.get('age3')
        doc.gender3 = request.POST.get('gender3')
        doc.school3 = request.POST.get('school3')
        doc.class3 = request.POST.get('class3')

        doc.name4 = request.POST.get('name4')
        doc.age4 = request.POST.get('age4')
        doc.gender4 = request.POST.get('gender4')
        doc.school4 = request.POST.get('school4')
        doc.class4 = request.POST.get('class4')

        doc.name5 = request.POST.get('name5')
        doc.age5 = request.POST.get('age5')
        doc.gender5 = request.POST.get('gender5')
        doc.school5 = request.POST.get('school5')
        doc.class5 = request.POST.get('class5')

        doc.admission_form = request.POST.get('admission_form')
        doc.admission_form_remarks = request.POST.get('admission_form_remarks')
        doc.school_leaving_certificate = request.POST.get('school_leaving_certificate')
        doc.school_leaving_certificate_remarks = request.POST.get('school_leaving_certificate_remarks')
        doc.bonafide_certificate = request.POST.get('bonafide_certificate')
        doc.bonafide_certificate_remarks = request.POST.get('bonafide_certificate_remarks')
        doc.birth_certificate = request.POST.get('birth_certificate')
        doc.birth_certificate_remarks = request.POST.get('birth_certificate_remarks')
        doc.caste_certificate = request.POST.get('caste_certificate')
        doc.caste_certificate_remarks = request.POST.get('caste_certificate_remarks')
        doc.all_documents = request.POST.get('all_documents')
        doc.all_documents_remarks = request.POST.get('all_documents_remarks')
        doc.ration_card = request.POST.get('ration_card')
        doc.ration_card_remarks = request.POST.get('ration_card_remarks')
        doc.student_adhar_certificate = request.POST.get('student_adhar_certificate')
        doc.student_adhar_certificate_remarks = request.POST.get('student_adhar_certificate_remarks')
        doc.father_adhar_certificate = request.POST.get('father_adhar_certificate')
        doc.father_adhar_certificate_remarks = request.POST.get('father_adhar_certificate_remarks')
        doc.mother_adhar_certificate = request.POST.get('mother_adhar_certificate')
        doc.mother_adhar_certificate_remarks = request.POST.get('mother_adhar_certificate_remarks')
        doc.save()

        return JsonResponse({'message': 'Student details updated successfully'})

    return render(request,"student_profile.html")
   



def get_sections_and_subjects(request):
    class_id = request.GET.get("class_id")
    section_id = request.GET.get("section_id")
    teacher = Teacher.objects.get(custid=request.user)

    sections = Section.objects.filter(class_assigned_id=class_id).values("id", "name")
    
    subjects = []
    if class_id and section_id:
        subjects = teacher.assigned_subjects1.filter(class_assigned_id=class_id).values("id", "name")

    return JsonResponse({"sections": list(sections), "subjects": list(subjects)})


from datetime import date
def admin_login(request):
    try:
        a1 = SchoolDetails.objects.get(custid=request.user)
    except SchoolDetails.DoesNotExist:
        a1 = None 
    std = studentadmission.objects.filter(school=a1).count()
    

    std1 = studentadmission.objects.filter(school=a1, admissiondate=date.today()).count()
    teach=Teacher.objects.filter(school=a1).count()
    clas=Class.objects.filter(school=a1).count()
    sec=Section.objects.filter(school=a1).count()
    total_fee = student_fee_Amount.objects.aggregate(total=models.Sum('total_amount'))['total'] or 0
    amount = StudentPayment.objects.aggregate(total=Sum('amount1'))['total'] or 0
    balance_amount = total_fee - amount
    return render(request,"admin_base.html",{'std':std,'teach':teach,'clas':clas,'sec':sec,'total_fee':total_fee,'amount':amount,'balance_amount':balance_amount,'std1':std1})


def admin_insert_fee(request):
    if request.method == "POST":
        std_class = request.POST.get('std_class')
        amount = request.POST.get('amount')
        if std_class and amount:
            admin_fee_structure.objects.create(std_class=std_class, amount=amount)
            return HttpResponse('inserted....')
    return render(request, 'admin_insert_fee.html')


def display_fee(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest': 
        class_name = request.GET.get('class_name')
        fee = admin_fee_structure.objects.filter(std_class=class_name).first()
        return JsonResponse({'amount': fee.amount if fee else ''})

    fees = admin_fee_structure.objects.all()
    return render(request, 'display_fee.html', {'fees': fees})



import uuid
from datetime import datetime
from django.contrib.auth.hashers import make_password
import pandas as pd

def bulk_insert_student_admission(request):
    try:
        a1 = SchoolDetails.objects.get(custid=request.user)
    except SchoolDetails.DoesNotExist:
        messages.error(request, "School details not found!")
        
    if request.method == 'POST' and request.FILES['excel_file']:
        excel_file = request.FILES['excel_file']
        df = pd.read_excel(excel_file)
        print("DataFrame head:")
        print(df.head())  # Debug output to see all columns

        for index, row in df.iterrows():
            try:
                # Handle username
                username = row.get('username')  # Use .get() to avoid KeyError
                if pd.isna(username) or str(username).lower() == 'nan':
                    username = f"student_{uuid.uuid4().hex[:8]}"  # Unique username

                # Handle email
                email = row.get('email')
                if pd.isna(email) or str(email).lower() == 'nan':
                    email = f"{username}@example.com"  # Unique email based on username

                # Handle password
                password = row.get('password')
                if pd.isna(password) or str(password).lower() == 'nan':
                    password_str = uuid.uuid4().hex[:10]  # Random 10-character password
                else:
                    password_str = str(password)  # Convert to string if provided

                # Create CustomUser
                user = CustomUser.objects.create(
                    username=username,
                    email=email,
                    password=make_password(password_str),  # Hash the password
                    role=row.get('role', 'student')  # Default role if missing
                )

                # Handle dateofbirth
                dob = row.get('dateofbirth')
                if pd.isna(dob):
                    dob_str = None
                elif isinstance(dob, datetime):
                    dob_str = dob.strftime('%Y-%m-%d')
                else:
                    dob_str = str(dob).strip()
                    try:
                        datetime.strptime(dob_str, '%Y-%m-%d')
                    except ValueError:
                        return JsonResponse({"error": f"Error processing row {index}: Invalid date format for dateofbirth (use YYYY-MM-DD)"}, status=400)

                # Handle classs and section (not provided in Excel, so set to None)
                classs_instance = None  # Since classs column isn’t in Excel
                section_instance = None  # Since section column isn’t in Excel

                # Create studentadmission
                student = studentadmission.objects.create(
                    registrationno=row.get('registrationno', f"REG_{uuid.uuid4().hex[:6]}"),
                    studentname=row.get('studentname', "Unnamed"),
                    classs=classs_instance,  # Will be None
                    section=section_instance,  # Will be None
                    gender=row.get('gender'),
                    house=row.get('house'),
                    address=row.get('address'),
                    mbno=row.get('mbno'),
                    dateofbirth=dob_str,
                    custid=user,
                    school=a1
                )

                # Rest of your related objects
                EducationDetail.objects.create(stdid=student, custid=user,school=a1)
                Previousschooling.objects.create(stdid=student, custid=user,school=a1)
                FamilyDetails.objects.create(
                    stdid=student,
                    father_name=row.get('father_name'),
                    mother_name=row.get('mother_name'),
                    custid=user,
                    school=a1
                )
                SiblingDocumentSubmission.objects.create(stdid=student, custid=user,school=a1)
                TransportInformation.objects.create(stdid=student, custid=user,school=a1)
                student_fee_Amount.objects.create(stdid=student, custid=user,school=a1)

            except Exception as e:
                return JsonResponse({"error": f"Error processing row {index}: {str(e)}"}, status=400)

        return JsonResponse({"message": "Bulk data insertion successful."})


def student_updatefee(request):
    try:
        a1 = SchoolDetails.objects.get(custid=request.user)
    except SchoolDetails.DoesNotExist:
        messages.error(request, "School details not found!")
        return redirect('admin_dashboard')  
    search_query = request.GET.get('search', '')  
    page_number = request.GET.get('page', 1)  

    
    if search_query:
        students = studentadmission.objects.filter(
            Q(registrationno__icontains=search_query) | 
            Q(studentname__icontains=search_query) | 
            Q(classs__icontains=search_query)
        )
    else:
        students = studentadmission.objects.filter(school=a1)

    # Paginate the student records
    paginator = Paginator(students, 10)  # Show 10 records per page
    students_page = paginator.get_page(page_number)

    # Fetch related data based on student ID
    education_details = {e.stdid_id: e for e in EducationDetail.objects.filter(school=a1)}
    previous_schools = {p.stdid_id: p for p in Previousschooling.objects.filter(school=a1)}
    family_details = {f.stdid_id: f for f in FamilyDetails.objects.filter(school=a1)}
    sibling_docs = {s.stdid_id: s for s in SiblingDocumentSubmission.objects.filter(school=a1)}
    transport_info = {t.stdid_id: t for t in TransportInformation.objects.filter(school=a1)}

    # Combine data while handling missing values
    combined_data = [
        (
            student,
            education_details.get(student.id, None),
            previous_schools.get(student.id, None),
            family_details.get(student.id, None),
            sibling_docs.get(student.id, None),
            transport_info.get(student.id, None),
        )
        for student in students_page
    ]

    # Check if any student is found
    no_data_found = not students.exists()

    return render(request, "updatefee.html", {
        'combined_data': combined_data, 
        'no_data_found': no_data_found, 
        'search_query': search_query,
        'students_page': students_page, 
        'a1':a1
    })



def edit_fee_view(request, id):
    try:
        a1 = SchoolDetails.objects.get(custid=request.user)
    except SchoolDetails.DoesNotExist:
        messages.error(request, "School details not found!")
        return redirect('admin_dashboard')
    fee_record = get_object_or_404(student_fee_Amount, stdid_id=id)

    o = student_fee_Amount.objects.filter(stdid_id=id).first()

    return render(request, "edit_fee.html", {"fee_record": fee_record,'o':o,'a1':a1})

def update_fee_view(request, id):
    if request.method == "POST":
        fee_record = get_object_or_404(student_fee_Amount, stdid_id=id)

        amount = int(request.POST.get("amount", 0))
        category = request.POST.get("category")

        percentage_map = {
            "admin": (0.50, "50%"),
            "staff": (0.25, "25%"),
            "normal": (0.10, "10%"),
        }

        discount_percentage_value, discount_percentage_label = percentage_map.get(category, (0, "0%"))
        discount = int(amount * discount_percentage_value)
        total_amount = amount - discount

        part = total_amount // 3
        remainder = total_amount % 3
        parts = [part, part, part]
        for i in range(remainder):
            parts[i] += 1

        # Update the existing record
        fee_record.original_amount = amount
        fee_record.discount = discount
        fee_record.discount_percentage = discount_percentage_label
        fee_record.total_amount = total_amount
        fee_record.part1 = parts[0]
        fee_record.part2 = parts[1]
        fee_record.part3 = parts[2]
        fee_record.category = category
        fee_record.save()

        return redirect("student_updatefee")  # Redirect to fee list or any page

    return render(request,"edit_fee.html")




# Initialize Razorpay Client
client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))


def student_fee_view(request, id):

    fd = get_object_or_404(student_fee_Amount, id=id)

    family_details = FamilyDetails.objects.filter(stdid=fd.stdid).first()

    if request.method == "POST":
        admissionno = request.POST.get('admissionno')
        fullname = request.POST.get('fullname')
        fathername = request.POST.get('fathername')
        mobilenumber = request.POST.get('mobilenumber')
        std_class = request.POST.get("std_class")
        
        try:
            amount1 = float(request.POST.get("amount", 0)) * 100  # Convert to paisa
        except ValueError:
            amount1 = 0

        if amount1 <= 0:
            return render(request, "student_fee_view.html", {
                'fd': fd,
                'family_details': family_details,
                'error_message': "Invalid amount. Please enter a valid price."
            })

        # Create Razorpay Order
        order_data = {
            'amount': int(amount1),  # Razorpay needs amount in paisa
            'currency': 'INR',
            'receipt': f'order_{id}',
            'payment_capture': '1',  # Auto capture payment
            'notes': {
                'fullname': fullname,
                'fathername': fathername,
                'std_class': std_class,
                'mobilenumber': mobilenumber,
                'admissionno': admissionno
            }
        }

        try:
            order = client.order.create(order_data)
        except Exception as e:
            return render(request, "student_fee_view.html", {
                'fd': fd,
                'error_message': f"Error creating Razorpay order: {str(e)}"
            })

        context = {
            'order': order,
            'order_id': order['id'],
            'fullname': fullname,
            'fathername': fathername,
            'std_class': std_class,
            'mobilenumber': mobilenumber,
            'admissionno': admissionno,
            'amount1': amount1 / 100,  # Convert back to rupees
            'razorpay_key': settings.RAZORPAY_API_KEY,
        }

        return render(request, "student_fee_receipt.html", context)

    return render(request, "student_fee_view.html", {'fd': fd,'family_details': family_details})


def student_fee_status(request):
    if request.method == "POST":
        payment_id = request.POST.get('razorpay_payment_id')
        order_id = request.POST.get('razorpay_order_id')
        signature = request.POST.get('razorpay_signature')

        params_dict = {
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }

        try:
            # Verify the Razorpay signature
            client.utility.verify_payment_signature(params_dict)

            # Capture form data
            fullname = request.POST.get('fullname')
            fathername = request.POST.get('fathername')
            std_class = request.POST.get('std_class')
            mobilenumber = request.POST.get('mobilenumber')
            admissionno = request.POST.get('admissionno')
            amount1 = float(request.POST.get('amount1'))

            # Save payment details to the database
            order_entry = StudentPayment.objects.create(
                fullname=fullname,
                fathername=fathername,
                std_class=std_class,
                mobilenumber=mobilenumber,
                admissionno=admissionno,
                amount1=amount1,
                transaction_id=payment_id,
                payment_mode="Online"
            )

            # Pass all data to the receipt template
            context = {
                'status': 'success',
                'fullname': fullname,
                'fathername': fathername,
                'std_class': std_class,
                'mobilenumber': mobilenumber,
                'admissionno': admissionno,
                'amount1': amount1,
                'transaction_id': payment_id,
                'payment_mode': "Online",
                'rec_no': order_entry.id
            }
            return render(request, "student_fee_receipt.html", context)

        except razorpay.errors.SignatureVerificationError:
            return render(request, "student_fee_receipt.html", {'status': 'failure'})

    return HttpResponse("Invalid request")





def studentfee_download_receipt(request):
    admissionno = request.GET.get("admissionno")
    fullname = request.GET.get("fullname")
    fathername = request.GET.get("fathername")
    std_class = request.GET.get("std_class")
    amount1 = request.GET.get("amount1")
    mobilenumber=request.GET.get("mobilenumber")
    current_date = datetime.now().strftime("%Y-%m-%d")


    # Construct absolute path for the image
    image_path = os.path.join(settings.STATIC_URL, "img/Recipt 1.jpg")
    absolute_image_path = request.build_absolute_uri(image_path)
    
    html_content = f"""
    
    <!DOCTYPE html>
    <html>
    <head>
        <style>
    body {{
        font-family:Georgia, 'Times New Roman', Times, serif !important;
        
        
    }}
    .sz{{
        font-size:14px;
    }}
    .receipt-container {{
        width: 800px;
        margin: auto;
       
        padding: 20px;
    }}
    .header {{
        text-align: center;
        border-bottom: 2px solid #000;
        
    }}
    .header h1 {{
        color: green;
        margin: 5px 0;
    }}
    .school-info {{
        text-align: center;
        font-size: 14px;
    }}
    .details {{
        margin-top: 20px;
    }}
    .details-table {{
        width: 100%;
        margin-left: 80px;
        border-collapse: collapse;
        font-size: small;
        color: #000;
    }}
    .details-table td {{
        padding: 5px;
    }}
    .fee-table {{
        width: 100%;
        border-collapse: collapse;
        margin-top: 20px;
        font-size: small;
        color: #000;
    }}
    .fee-table th, .fee-table td {{
        border: 1px solid black;
        padding: 8px;
        text-align: left;
    }}
    .fee-table th {{
        background-color: #ddd;
    }}
    .total {{
        text-align: right;
        margin-top: 10px;
        font-size: 16px;
        font-weight: bold;
    }}
    .balance {{
        margin-top: 10px;
        font-weight: bold;
    }}
    .signature {{
        text-align: right;
        margin-top: 20px;
        font-weight: bold;
    }}
    #table{{
        font-size: medium;
    
    }}
</style>
        <title>Payment Receipt</title>
    </head>
    <body>
        <div class="receipt-container">
    <div class="header">
        <div style="display: flex; align-items: center; justify-content: center;">
            <div>
                 <img src="{absolute_image_path}" width="760" height="150">

            </div>
        </div>
    </div>
    

    <h2 style="text-align:center;font-size: 18px;" class="month-heading">FEE Payment Receipt</h2>

    <table class="details-table" >
        <tr>
            <td><p class="sz"><strong>Adm. No.:</strong> { admissionno }</p></td>
            <td><p class="sz"><strong>Date:</strong> {current_date}</p></td>
        </tr>
        <tr>
            <td><p class="sz"><strong>Student Name:</strong> { fullname }</p></td>
        </tr>
        <tr>
            <td><p class="sz"><strong>Father's Name:</strong> { fathername }</p></td>
            <td><p class="sz"><strong>Mobile No:</strong> { mobilenumber }</p></td>
        </tr>
        <tr>
            <td><p class="sz"><strong>Class & Section:</strong> { std_class }</p></td>
        </tr>
        
    </table>

    <table class="fee-table">
          <tr>
             <th>Sr. No.</th>
             <th>Grand Total</th>
         </tr>
         <tr>
             <td><p class="sz">1</p></td>
             <td><p class="sz">{ amount1 }</p></td>
         </tr>
    </table>
<br>
<br>

    <div class="signature" style="color: #000;">
        Accountant Signature
    </div>
</div>
    </body>
    </html>
    """

   
    pdf_buffer = BytesIO()
    pisa_status = pisa.CreatePDF(html_content, dest=pdf_buffer)

   
    if pisa_status.err:
        return HttpResponse("Error generating PDF", status=500)

    pdf_buffer.seek(0)
    response = HttpResponse(pdf_buffer, content_type="application/pdf")
    response["Content-Disposition"] = "attachment; filename=receipt.pdf"
    return response



def insert_teacher(request):

  
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        role = request.POST['role']
        if CustomUser.objects.filter(username=username).exists():
            return render(request, 'teacher.html', {'error': 'Username already exists'})

        user = CustomUser.objects.create(
            username=username,
            email=email,
            password=make_password(password),
            role=role
        )
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        date_of_birth = request.POST.get('date_of_birth')
        subjects = request.POST.get('subjects')
        Teacher.objects.create(
            
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            date_of_birth=date_of_birth,
            subjects=subjects,
            custid=user,
        )



    return render(request, 'teacher.html')



from django.shortcuts import render, redirect
from django.db.models import Q

def assign_teacher_to_class(request):
    # Get all assigned teacher IDs
   
    try:
        a1 = SchoolDetails.objects.get(custid=request.user)
    except SchoolDetails.DoesNotExist:
        messages.error(request, "School details not found!")
        return redirect('admin_dashboard')  
    
    assigned_teacher_ids = AssignedClass.objects.values_list('teacher_id', flat=True)
    
    # Get all assigned class IDs and section IDs
    assigned_class_ids = AssignedClass.objects.values_list('class_assigned_id', flat=True)
    assigned_section_ids = AssignedClass.objects.values_list('section_id', flat=True)


    teachers = Teacher.objects.filter(school=a1).exclude(id__in=assigned_teacher_ids)
    classes = Class.objects.filter(school=a1).exclude(id__in=assigned_class_ids)
    sections = Section.objects.filter(school=a1).exclude(id__in=assigned_section_ids)

    if request.method == "POST":
        teacher_id = request.POST['teacher']
        class_id = request.POST['class_assigned']
        section_id = request.POST['section']

        teacher = Teacher.objects.get(id=teacher_id)
        selected_class = Class.objects.get(id=class_id)
        selected_section = Section.objects.get(id=section_id)

        AssignedClass.objects.create(
            teacher=teacher,
            custid=teacher.custid,
            class_assigned=selected_class,
            section=selected_section,
            school=a1
        )

        return redirect('assign_teacher_to_class')

    return render(request, "assign_teachers.html", {
        "teachers": teachers,
        "classes": classes,
        "sections": sections,
        'a1':a1
    })

from django.db.models import Prefetch

def class_teachers_list(request):
    try:
        a1 = SchoolDetails.objects.get(custid=request.user)
    except SchoolDetails.DoesNotExist:
        messages.error(request, "School details not found!")
        return redirect('admin_dashboard')  
    # Prefetch assigned classes and sections to reduce DB hits
    teachers = Teacher.objects.filter(school=a1).prefetch_related(
        Prefetch(
            'assignedfdegfregterclasses',  # Related name in AssignedClass
            queryset=AssignedClass.objects.select_related('class_assigned', 'section')
        )
    )

    return render(request, "class_teachers_list.html", {"teachers": teachers,'a1':a1})

from django.db.models import Q
from django.core.paginator import Paginator
from io import BytesIO
import openpyxl
from xhtml2pdf import pisa

def teachers_view(request):
    try:
        a1 = SchoolDetails.objects.get(custid=request.user)
    except SchoolDetails.DoesNotExist:
        messages.error(request, "School details not found!")
        return redirect('admin_dashboard')  # Redirect if school is not set up
    
    search_query = request.GET.get('search', '').strip()
    teachers = Teacher.objects.filter(school=a1)

    if search_query:
        teachers = teachers.filter(
            Q(first_name__icontains=search_query) | 
            Q(subjects__icontains=search_query)
        )

    paginator = Paginator(teachers, 5)  # 5 teachers per page
    page_number = request.GET.get('page')
    teachers_page = paginator.get_page(page_number)

    # Credentials export logic
    credentials = TeacherCredentials.objects.filter(school=a1)

    if request.method == 'POST':
        file_format = request.POST.get('file_format')
        form_password = request.POST.get('password', '')

        # Prepare data for export
        data = []
        for cred in credentials:
            data.append({
                'Username': cred.username,
                'Email': cred.email,
                'Role': cred.role,
                'Teacher Name': f"{cred.teacherid.first_name} {cred.teacherid.last_name}" if cred.teacherid else 'N/A',
                'Phone': cred.teacherid.phone if cred.teacherid else 'N/A',
                'Original Password': cred.password,
                'Form Password': form_password,
                'Created At': cred.teacherid.created_at.strftime('%Y-%m-%d %H:%M:%S') if cred.teacherid else 'N/A'
            })

        if file_format == 'excel':
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Teacher Credentials"
            headers = ['Username', 'Email', 'Role', 'Teacher Name', 'Phone', 'Original Password', 'Form Password', 'Created At']
            ws.append(headers)
            for row in data:
                ws.append([row[h] for h in headers])
            buffer = BytesIO()
            wb.save(buffer)
            buffer.seek(0)
            response = HttpResponse(
                buffer.getvalue(),
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = 'attachment; filename="teacher_credentials.xlsx"'
            return response

        elif file_format == 'pdf':
            html = """
            <html>
            <head>
                <style>
                    table { width: 100%; border-collapse: collapse; }
                    th, td { border: 1px solid black; padding: 8px; text-align: left; }
                    th { background-color: #f2f2f2; }
                </style>
            </head>
            <body>
                <h1>Teacher Credentials</h1>
                <table>
                    <tr>
                        <th>Username</th><th>Email</th><th>Role</th><th>Teacher Name</th>
                        <th>Phone</th><th>Original Password</th><th>Form Password</th><th>Created At</th>
                    </tr>
            """
            for item in data:
                html += f"""
                    <tr>
                        <td>{item['Username']}</td><td>{item['Email']}</td><td>{item['Role']}</td>
                        <td>{item['Teacher Name']}</td><td>{item['Phone']}</td><td>{item['Original Password']}</td>
                        <td>{item['Form Password']}</td><td>{item['Created At']}</td>
                    </tr>
                """
            html += "</table></body></html>"

            buffer = BytesIO()
            pisa_status = pisa.CreatePDF(html, dest=buffer)
            if not pisa_status.err:
                buffer.seek(0)
                response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="teacher_credentials.pdf"'
                return response
            else:
                # Handle PDF generation error (optional)
                context['error'] = "Error generating PDF"

    # Context for rendering the template
    context = {
        'tea': teachers_page,
        'search_query': search_query,
        'teachers_page': teachers_page,  # Renamed for clarity
        'no_data_found': search_query and not teachers.exists(),
        'credentials_list': credentials,
        'a1':a1
    }

    return render(request, 'teachers_view.html', context)

def edit_teacher(request, id):
    tea1 = get_object_or_404(Teacher, id=id)
    return render(request, "update_teacher.html", {'tea1': tea1})

def update_teacher(request, id):
    if request.method == 'POST':
        tea1 = get_object_or_404(Teacher, id=id)

        tea1.first_name = request.POST.get('first_name')
        tea1.last_name = request.POST.get('last_name')
        tea1.phone = request.POST.get('phone')
        tea1.date_of_birth = request.POST.get('date_of_birth')
        tea1.subjects = request.POST.get('subjects')
        tea1.profile = request.POST.get('profile')

        tea1.save()
        
        return redirect('teachers_view')

    return render(request, "update_teacher.html", {'tea1': tea1})


def delete_teacher(request,id):
    try:
        a1 = SchoolDetails.objects.get(custid=request.user)
    except SchoolDetails.DoesNotExist:
        messages.error(request, "School details not found!")
        return redirect('admin_dashboard')  # Redirect if school is not set up
    tea1=Teacher.objects.get(id=id,school=a1)
    tea1.delete()
    return redirect('teachers_view')


def student_family_details(request):
    if not request.user.is_authenticated:
        return redirect('login')

    try:
        i = studentadmission.objects.get(custid=request.user)
    except studentadmission.DoesNotExist:
        i = None  
    try:
        n = TransportInformation.objects.get(custid=request.user)
    except TransportInformation.DoesNotExist:
        n = None

    try:
        j = EducationDetail.objects.get(custid=request.user)
    except EducationDetail.DoesNotExist:
        j = None     

    try:
        k = Previousschooling.objects.get(custid=request.user)
    except Previousschooling.DoesNotExist:
        k = None    

    try:
        l = FamilyDetails.objects.get(custid=request.user)
    except FamilyDetails.DoesNotExist:
        l = None 

    try:
        m = SiblingDocumentSubmission.objects.get(custid=request.user)
    except SiblingDocumentSubmission.DoesNotExist:
        m = None    

    try:
        o = student_fee_Amount.objects.get(custid=request.user)
    except student_fee_Amount.DoesNotExist:
        o = None    

    try:
        assigned_class = AssignedClass.objects.get(custid=request.user)
        assigned_class_name = assigned_class.class_assigned.strip().lower()  # Normalize class name
        sec = assigned_class.section.strip().lower()  # Normalize section

        # Fetch students with matching class and section
        students = studentadmission.objects.filter(
            classs__iexact=assigned_class_name,
            section__iexact=sec
        )

        print(f"DEBUG: Assigned Class - '{assigned_class_name}', Section - '{sec}'")
        print(f"DEBUG: Found {students.count()} students")

    except AssignedClass.DoesNotExist:
        assigned_class = None
        students = None
        print("DEBUG: No AssignedClass found for this user.")    

    context = {
        'user': request.user,
        
        
        'i' : i,
        'j' : j,
        'k' : k,
        'l' : l,
        'm' : m,
        'n' : n,
        'o' : o,
        'p': assigned_class,
        'students': students, 
    }

    return render(request, 'student_family_details.html', context)

def student_transport_details(request):
    if not request.user.is_authenticated:
        return redirect('login')

    try:
        i = studentadmission.objects.get(custid=request.user)
    except studentadmission.DoesNotExist:
        i = None  
    try:
        n = TransportInformation.objects.get(custid=request.user)
    except TransportInformation.DoesNotExist:
        n = None

    try:
        j = EducationDetail.objects.get(custid=request.user)
    except EducationDetail.DoesNotExist:
        j = None     

    try:
        k = Previousschooling.objects.get(custid=request.user)
    except Previousschooling.DoesNotExist:
        k = None    

    try:
        l = FamilyDetails.objects.get(custid=request.user)
    except FamilyDetails.DoesNotExist:
        l = None 

    try:
        m = SiblingDocumentSubmission.objects.get(custid=request.user)
    except SiblingDocumentSubmission.DoesNotExist:
        m = None    

    try:
        o = student_fee_Amount.objects.get(custid=request.user)
    except student_fee_Amount.DoesNotExist:
        o = None    

    try:
        assigned_class = AssignedClass.objects.get(custid=request.user)
        assigned_class_name = assigned_class.class_assigned.strip().lower()  # Normalize class name
        sec = assigned_class.section.strip().lower()  # Normalize section

        # Fetch students with matching class and section
        students = studentadmission.objects.filter(
            classs__iexact=assigned_class_name,
            section__iexact=sec
        )

        print(f"DEBUG: Assigned Class - '{assigned_class_name}', Section - '{sec}'")
        print(f"DEBUG: Found {students.count()} students")

    except AssignedClass.DoesNotExist:
        assigned_class = None
        students = None
        print("DEBUG: No AssignedClass found for this user.")    

    context = {
        'user': request.user,
        
        
        'i' : i,
        'j' : j,
        'k' : k,
        'l' : l,
        'm' : m,
        'n' : n,
        'o' : o,
        'p': assigned_class,
        'students': students, 
    }

    return render(request, 'student_transport_details.html', context)
    
    
from django.shortcuts import render
from django.db.models import Sum
from .models import student_fee_Amount, StudentPayment 

def student_fee_management(request):
    try:
        i = studentadmission.objects.get(custid=request.user)
    except studentadmission.DoesNotExist:
        i = None
    try:
        o = student_fee_Amount.objects.get(custid=request.user) 
    except student_fee_Amount.DoesNotExist:
        o = None

    total_paid = 0
    paid1, paid2, paid3 = 0, 0, 0
    balance1, balance2, balance3 = 0, 0, 0

    if o:  
        payments = StudentPayment.objects.filter(custid=request.user).aggregate(total_paid=Sum('amount1'))
        total_paid = payments['total_paid'] or 0  
        
       
        balance1, balance2, balance3 = o.part1, o.part2, o.part3
        
       
        remaining_amount = total_paid
        if remaining_amount > 0:
            if remaining_amount >= o.part1:
                paid1 = o.part1
                remaining_amount -= o.part1
            else:
                paid1 = remaining_amount
                remaining_amount = 0

            if remaining_amount >= o.part2:
                paid2 = o.part2
                remaining_amount -= o.part2
            else:
                paid2 = remaining_amount
                remaining_amount = 0

            if remaining_amount >= o.part3:
                paid3 = o.part3
                remaining_amount -= o.part3
            else:
                paid3 = remaining_amount
                remaining_amount = 0
        
        # Calculate balance for each part
        balance1 = o.part1 - paid1
        balance2 = o.part2 - paid2
        balance3 = o.part3 - paid3

    context = {
        'user': request.user,
        'o': o,
        'total_paid': total_paid,
        'paid1': paid1,
        'paid2': paid2,
        'paid3': paid3,
        'balance1': balance1,
        'balance2': balance2,
        'balance3': balance3,
        'total_balance': balance1 + balance2 + balance3,
        'i':i
    }

    return render(request, 'student_fee_management.html', context)

from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def save_student_marks(request):
    if request.method == 'POST':
        try:
            # Get the logged-in teacher based on 'custid' (linked to CustomUser)
            teacher = Teacher.objects.get(custid=request.user)

            for key, value in request.POST.items():
                if key.startswith('marks_'):
                    student_id = key.split('_')[1]
                    student = studentadmission.objects.get(id=student_id)

                   
                    StudentMarks.objects.create(
                        student=student,
                        total_marks=int(value),
                        teacherid=teacher, 
                    )

            messages.success(request, "Marks saved successfully!")
        except Teacher.DoesNotExist:
            messages.error(request, "You are not assigned as a teacher.")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

    return redirect('dashboard')

from .models import Class, Section, Subject

def add_class(request):
    """ Add, Edit, and Delete Class """
    try:
        a1 = SchoolDetails.objects.get(custid=request.user)
    except SchoolDetails.DoesNotExist:
        messages.error(request, "School details not found!")
        return redirect('admin_dashboard')  # Redirect if school is not set up

    if request.method == "POST":
        class_id = request.POST.get('class_id')  # Check if it's an edit
        name = request.POST.get('name')

        if name:
            if class_id:  # Editing existing class
                class_obj = get_object_or_404(Class, id=class_id, school=a1)
                class_obj.name = name
                class_obj.save()
                messages.success(request, "Class updated successfully!")
            else:  # Adding new class
                if not Class.objects.filter(name=name, school=a1).exists():  # Prevent duplicates within the same school
                    Class.objects.create(name=name, school=a1)
                    messages.success(request, "Class added successfully!")
                else:
                    messages.error(request, "Class with this name already exists in your school!")

        return redirect('add_class')

    # Handle Delete
    if request.method == "GET" and 'delete_id' in request.GET:
        delete_id = request.GET.get('delete_id')
        class_obj = get_object_or_404(Class, id=delete_id, school=a1)
        class_obj.delete()
        messages.success(request, "Class deleted successfully!")
        return redirect('add_class')

    # Fetch all classes belonging to the logged-in admin's school
    classes = Class.objects.filter(school=a1).order_by('name')

    context = {
        'classes': classes,
        'a1': a1  # Pass school details
    }
    return render(request, 'add_class.html', context)


def add_section(request):
    """ Add, Edit, and Delete Section """
    try:
        a1 = SchoolDetails.objects.get(custid=request.user)
    except SchoolDetails.DoesNotExist:
        messages.error(request, "School details not found!")
        return redirect('admin_dashboard')  # Redirect if school is not set up
    
    classes = Class.objects.filter(school=a1).order_by('name')

    if request.method == "POST":
        section_id = request.POST.get('section_id')  # For editing
        class_id = request.POST.get('class_assigned')
        name = request.POST.get('name')

        if class_id and name:
            class_obj = get_object_or_404(Class, id=class_id,school=a1)

            if section_id:  # Edit existing section
                section = get_object_or_404(Section, id=section_id,school=a1)
                section.class_assigned = class_obj
                section.name = name
                section.save()
                messages.success(request, "Section updated successfully!")
            else:  # Add new section
                if not Section.objects.filter(class_assigned=class_obj, name=name,school=a1).exists():
                    Section.objects.create(class_assigned=class_obj, name=name,school=a1)
                    messages.success(request, "Section added successfully!")
                else:
                    messages.error(request, "Section already exists!")

        return redirect('add_section')

    # Handle Delete
    if request.method == "GET" and 'delete_id' in request.GET:
        delete_id = request.GET.get('delete_id')
        section = get_object_or_404(Section, id=delete_id,)
        section.delete()
        messages.success(request, "Section deleted successfully!")
        return redirect('add_section')

    sections = Section.objects.filter(school=a1).order_by('class_assigned__name', 'name')

    context = {
        'classes': classes,
        'sections': sections,
        'a1':a1
    }
    return render(request, 'add_section.html', context)



def add_subject(request):
    """ Add, Edit, and Delete Subjects """
    try:
        a1 = SchoolDetails.objects.get(custid=request.user)
    except SchoolDetails.DoesNotExist:
        messages.error(request, "School details not found!")
        return redirect('admin_dashboard')  # Redirect if school is not set up
    
    classes = Class.objects.filter(school=a1).order_by('name')
    sections = Section.objects.filter(school=a1).order_by('class_assigned__name', 'name')

    if request.method == "POST":
        subject_id = request.POST.get('subject_id')  # For editing
        class_id = request.POST.get('class_assigned')
        name = request.POST.get('name')

        if class_id and name:
            class_obj = get_object_or_404(Class, id=class_id)

            if subject_id:  # Edit existing subject
                subject = get_object_or_404(Subject, id=subject_id)
                subject.class_assigned = class_obj
                subject.name = name
                subject.save()
                messages.success(request, "Subject updated successfully!")
            else:  # Add new subject
                if not Subject.objects.filter(class_assigned=class_obj, name=name).exists():
                    Subject.objects.create(class_assigned=class_obj, name=name,school=a1)
                    messages.success(request, "Subject added successfully!")
                else:
                    messages.error(request, "Subject already exists!")

        return redirect('add_subject')

    # Handle Delete
    if request.method == "GET" and 'delete_id' in request.GET:
        delete_id = request.GET.get('delete_id')
        subject = get_object_or_404(Subject, id=delete_id)
        subject.delete()
        messages.success(request, "Subject deleted successfully!")
        return redirect('add_subject')

    subjects = Subject.objects.filter(school=a1).order_by('class_assigned__name', 'name')

    context = {
        'classes': classes,
        'subjects': subjects,
        'a1':a1
    }
    return render(request, 'add_subject.html', context)


def add_fee(request):
    """ Add, Edit, and Delete Fees """
    try:
        a1 = SchoolDetails.objects.get(custid=request.user)
    except SchoolDetails.DoesNotExist:
        messages.error(request, "School details not found!")
        return redirect('admin_dashboard')  # Redirect if school is not set up
    
    classes = Class.objects.filter(school=a1).order_by('name')

    if request.method == "POST":
        fee_id = request.POST.get('fee_id')  # For editing
        class_id = request.POST.get('class_assigned')
        amount = request.POST.get('amount')

        if class_id and amount:
            class_obj = get_object_or_404(Class, id=class_id)

            if fee_id:  # Edit existing fee
                fee = get_object_or_404(admin_fee_structure, id=fee_id)
                fee.class_assigned = class_obj
                fee.amount = amount
                fee.save()
                messages.success(request, "Fee updated successfully!")
            else:  # Add new fee
                if not admin_fee_structure.objects.filter(class_assigned=class_obj, amount=amount).exists():
                    admin_fee_structure.objects.create(
                        class_assigned=class_obj,
                        amount=amount,
                        school=a1
                    )
                    messages.success(request, "Fee added successfully!")
                else:
                    messages.error(request, "Fee already exists for this class and section!")

        return redirect('add_fee')

    # Handle Delete
    if request.method == "GET" and 'delete_id' in request.GET:
        delete_id = request.GET.get('delete_id')
        fee = get_object_or_404(admin_fee_structure, id=delete_id)
        fee.delete()
        messages.success(request, "Fee deleted successfully!")
        return redirect('add_fee')

    fees = admin_fee_structure.objects.filter(school=a1).order_by('class_assigned__name')

    context = {
        'classes': classes,
        'fees': fees,'a1':a1
    }
    return render(request, 'add_fee.html', context)



def class_section_view(request):
    classes = Class.objects.all()
    return render(request, 'class_section.html', {'classes': classes})

def get_sections_and_fee(request):
    try:
        a1 = SchoolDetails.objects.get(custid=request.user)
    except SchoolDetails.DoesNotExist:
        messages.error(request, "School details not found!")
        return redirect('admin_dashboard')  # Redirect if school is not set up
    
    
    class_id = request.GET.get('class_id')
    sections = Section.objects.filter(class_assigned_id=class_id,school=a1).values('id', 'name')
    fee = admin_fee_structure.objects.filter(class_assigned_id=class_id,school=a1).first()
    
    fee_amount = fee.amount if fee else 0
    
    return JsonResponse({'sections': list(sections), 'fee': fee_amount})

def save_fee_record(request):
    if request.method == 'POST':
        class_id = request.POST.get('class_id')
        section_id = request.POST.get('section_id')
        amount = request.POST.get('amount')

        if class_id and section_id and amount:
            class_obj = Class.objects.get(id=class_id)
            section_obj = Section.objects.get(id=section_id)

            StudentFeeRecord.objects.create(
                class_assigned=class_obj,
                section=section_obj,
                amount=int(amount)
            )
            return JsonResponse({'status': 'success', 'message': 'Data saved successfully'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Missing data'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})



def get_sections(request):
    class_id = request.GET.get('class_id')
    
    if class_id:
        sections = Section.objects.filter(class_assigned_id=class_id).values('id', 'name')
        return JsonResponse({"sections": list(sections)})
    
    return JsonResponse({"sections": []})  # Return empty list if no class_id provided
from django.http import JsonResponse
from .models import admin_fee_structure

def get_fee_amount(request):
    try:
        a1 = SchoolDetails.objects.get(custid=request.user)
    except SchoolDetails.DoesNotExist:
        messages.error(request, "School details not found!")
        return redirect('admin_dashboard')  # Redirect if school is not set up
    
  
    class_id = request.GET.get('class_id')

    if class_id:
        try:
            fee_structure = admin_fee_structure.objects.get(class_assigned_id=class_id,school=a1)
            amount = fee_structure.amount
        except admin_fee_structure.DoesNotExist:
            amount = 0  # Default to 0 if no fee structure is found
        return JsonResponse({"amount": amount})

    return JsonResponse({"amount": 0})  # Default response if no class_id is provided



def class_selection_view(request):
    classes = Class.objects.all()
    sections = Section.objects.all()
    subjects = Subject.objects.all()
    return render(request, 'class_section.html', {
        'classes': classes, 
        'sections': sections, 
        'subjects': subjects
    })


def assign_teacher(request):
    try:
        a1 = SchoolDetails.objects.get(custid=request.user)
    except SchoolDetails.DoesNotExist:
        messages.error(request, "School details not found!")
        return redirect('admin_dashboard')  # Redirect if school is not set up
    
    if request.method == "POST":
        username = request.POST.get('username', None)
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        date_of_birth = request.POST.get('date_of_birth', None)
        role = request.POST.get('role', 'student')

        if not username:
            while True:
                username = f"user_{get_random_string(6)}"
                if not CustomUser.objects.filter(username=username).exists():
                    break  
        if not email:
            email = f"{username}@example.com"
        if not password:
            password = get_random_string(8)

        hashed_password = make_password(password)

     
        # ✅ Get selected subjects
        assigned_subject_ids = request.POST.getlist("assigned_subjects")

        # ✅ Check if subjects are already assigned
        existing_assigned_subjects = Teacher.objects.filter(assigned_subjects1__id__in=assigned_subject_ids).distinct()

        if existing_assigned_subjects.exists():
            assigned_subject_names = Subject.objects.filter(school=a1,id__in=assigned_subject_ids).values_list('name', flat=True)
            error_message = f"Subjects already assigned to another teacher: {', '.join(assigned_subject_names)}. Please choose different subjects."
            messages.error(request, error_message)
            return redirect("assign_teacher")  # Redirect back with error

          # Create the user
        user = CustomUser.objects.create(
            username=username,
            email=email,
            password=hashed_password,
            role=role
        )

     
        teacher = Teacher.objects.create(
            custid=user,
            school=a1,
            first_name=request.POST.get("first_name"),
            last_name=request.POST.get("last_name"),
            email=email,
            date_of_birth=request.POST.get("date_of_birth"),
            phone=request.POST.get("phone")
        )
        TeacherCredentials.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            password=password,
            role=user.role,
            teacherid=teacher,
            school=a1
        )

        teacher.assigned_classes1.set(Class.objects.filter(school=a1,id__in=request.POST.getlist("assigned_classes")))
        teacher.assigned_sections1.set(Section.objects.filter(school=a1,id__in=request.POST.getlist("assigned_sections")))
        teacher.assigned_subjects1.set(Subject.objects.filter(school=a1,id__in=assigned_subject_ids))

        return redirect("teachers_view")  # Redirect after saving

    classes = Class.objects.filter(school=a1)
    return render(request, "class_section.html", {"classes": classes,'a1':a1})


def teacher_login_list(request):
    try:
        a1 = SchoolDetails.objects.get(custid=request.user)
    except SchoolDetails.DoesNotExist:
        messages.error(request, "School details not found!")
        return redirect('admin_dashboard')  # Redirect if school is not set up
    obj=Teacher.objects.filter(school=a1)
    return render(request, "teacher_login_list.html", {
        'obj': obj, 
        'a1':a1
    })



def teacher_login_edit(request, id):
        try:
            a1 = SchoolDetails.objects.get(custid=request.user)
        except SchoolDetails.DoesNotExist:
            messages.error(request, "School details not found!")
            return redirect('admin_dashboard') 
    
        ob = CustomUser.objects.get(id=id)
        ob1 = Teacher.objects.get(custid=id)
        ob1.assigned_classes1.prefetch_related()
        ob1.assigned_sections1.prefetch_related()

        return render(request, "teacher_login_update.html", {'ob': ob,'ob1':ob1,'a1':a1})


def teacher_update_login(request, id):
    user = get_object_or_404(CustomUser, id=id)
  
    student_credentials = TeacherCredentials.objects.filter(user=user).first()

    if request.method == 'POST':
        username = request.POST.get('username', user.username)
        email = request.POST.get('email', user.email)
        password = request.POST.get('password', None)
        role = request.POST.get('role', user.role)

        if CustomUser.objects.filter(username=username).exclude(id=user.id).exists():
            return render(request, 'teacher_login_update.html', {'error': 'Username already exists', 'user': user})

        user.username = username
        user.email = email
        user.role = role
        
        if password: 
            user.password = make_password(password)
        
        user.save()

        if student_credentials:
            student_credentials.username = username
            student_credentials.email = email
            student_credentials.role = role
            
            if password:  
                student_credentials.password = password  

            student_credentials.save()

        return redirect('teacher_login_list')  

    return render(request, 'teacher_login_update.html', {'user': user})    




def insert_exam(request):
    """ Manage exams with add, edit, and delete functionality """
    try:
        a1 = SchoolDetails.objects.get(custid=request.user)
    except SchoolDetails.DoesNotExist:
        a1 = None 
    
    if request.method == "POST":
        exam_id = request.POST.get("exam_id")  # For editing
        exam_name = request.POST.get("examname")

        if exam_name:
            if exam_id:  # Editing
                # Use a different variable name for the queried object to avoid conflicts
                exam_instance = get_object_or_404(exam, id=exam_id)
                exam_instance.examname = exam_name
                exam_instance.save()
                messages.success(request, "Exam updated successfully!")
            else:  # Adding a new exam
                if not exam.objects.filter(examname=exam_name,school=a1).exists():
                    exam.objects.create(examname=exam_name,school=a1)
                    messages.success(request, "Exam added successfully!")
                else:
                    messages.error(request, "Exam with this name already exists!")

        return redirect('insert_exam')

    # Handle Delete
    if request.method == "GET" and 'delete_id' in request.GET:
        delete_id = request.GET.get('delete_id')
        exam_instance = get_object_or_404(exam, id=delete_id)
        exam_instance.delete()
        messages.success(request, "Exam deleted successfully!")
        return redirect('insert_exam')

    # Fetch all exams for display using a different variable name
    exams = exam.objects.filter(school=a1).order_by('examname')

    return render(request, "insertexam.html", {"exams": exams,'a1':a1})


def get_sections_subjects(request):
    class_ids = request.GET.getlist('class_ids[]')

    # Fetch all sections for selected classes
    sections = Section.objects.filter(class_assigned__id__in=class_ids).values('id', 'name')

    # Fetch all subjects for selected classes
    subjects = Subject.objects.filter(class_assigned__id__in=class_ids).values('id', 'name')

    # Get assigned subjects per section
    assigned_subjects_by_section = {}
    for section in sections:
        section_id = section["id"]
        assigned_subjects = Teacher.objects.filter(assigned_sections1=section_id).values_list("assigned_subjects1__id", flat=True)
        assigned_subjects_by_section[section_id] = list(assigned_subjects)

    return JsonResponse({
        'sections': list(sections),  
        'subjects': list(subjects),  
        'assigned_subjects_by_section': assigned_subjects_by_section  # Track assigned subjects per section
    })


def get_subjects_by_section(request):
    section_ids = request.GET.getlist('section_ids[]')

    subjects = Subject.objects.filter(class_assigned__sections__id__in=section_ids).distinct().values('id', 'name')

    # Get already assigned subjects per section
    assigned_subjects = Teacher.objects.filter(assigned_sections1__id__in=section_ids).values_list('assigned_subjects1__id', flat=True)

    subjects_list = []
    for subject in subjects:
        subject["assigned"] = subject["id"] in assigned_subjects  # Mark if assigned
        subjects_list.append(subject)

    return JsonResponse({'subjects': subjects_list})



def classteacherstudent(request):
    try:
        fm = Teacher.objects.get(custid=request.user)
    except Teacher.DoesNotExist:
        fm = None 

    if fm is not None:
        try:
            headings = teacherdashboardheading.objects.filter(school=fm.school).prefetch_related('teachersubmenu_set')
        except teacherdashboardheading.DoesNotExist:
            headings = None
    else:
        headings = None

    try:
        assigned_class = AssignedClass.objects.get(custid=request.user)
        assigned_class_name = assigned_class.class_assigned_id
        sec = assigned_class.section_id

        # Fetch students with matching class and section
        students = studentadmission.objects.filter(
            classs_id=assigned_class_name,
            section_id=sec
        )

        print(f"DEBUG: Assigned Class - '{assigned_class_name}', Section - '{sec}'")
        print(f"DEBUG: Found {students.count()} students")

    except AssignedClass.DoesNotExist:
        assigned_class = None
        students = None
        print("DEBUG: No AssignedClass found for this user.")

    return render(request,"classteacherstd.html",{'students':students,'headings':headings,'fm':fm})



from django.utils.timezone import now

def save_attendance(request):
    if request.method == 'POST':
        teacher = Teacher.objects.get(custid=request.user)

        student_ids = request.POST.getlist('student_id[]')
        attendance_status = request.POST.getlist('attendance_status[]')

        for student_id, status in zip(student_ids, attendance_status):
            student = studentadmission.objects.get(id=student_id)

            # Get or create attendance record for the same date
            attendance, created = Attendance.objects.get_or_create(
                student=student,
                teacher=teacher,
                date=now().date(),  # Filter by student, teacher, and date
                defaults={'status': status, 'custid': student.custid}  # Set defaults if new
            )

            # Update the status if the record already exists
            if not created:
                attendance.status = status
                attendance.save()

        return redirect('classteacherstudent')

    return redirect('classteacherstudent')


from datetime import datetime

def student_attendence_management(request):
    try:
        i = studentadmission.objects.get(custid=request.user)
    except studentadmission.DoesNotExist:
        i = None
    o = None  # Initially, no records

    if request.method == "GET" and 'search_date' in request.GET:
        search_date = request.GET.get('search_date')  # Get the selected date from the form
        try:
            formatted_date = datetime.strptime(search_date, "%Y-%m-%d").date()  # Convert to date format
            o = Attendance.objects.filter(custid=request.user, date=formatted_date)  # Filter attendance by date
        except ValueError:
            o = None  # If invalid date format, return no records

    return render(request, 'student_attendence_management.html', {'o': o,'i':i})


def student_attendance_management(request):
    try:
        a1 = SchoolDetails.objects.get(custid=request.user)
    except SchoolDetails.DoesNotExist:
        messages.error(request, "School details not found!")
        return redirect('admin_dashboard')
    classes = Class.objects.filter(school=a1)
    sections = Section.objects.filter(school=a1)
    # attendance_records = None  # Initially, no records

    # if request.method == "GET" and 'class_id' in request.GET and 'section_id' in request.GET and 'date' in request.GET:
    #     class_id = request.GET.get('class_id')
    #     section_id = request.GET.get('section_id')
    #     date_str = request.GET.get('date')

    #     try:
    #         selected_date = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else None
    #     except ValueError:
    #         selected_date = None

    #     # Get students in the selected class and section
    #     students = studentadmission.objects.filter(classs_id=class_id, section_id=section_id)
        
    #     # Get attendance records for the filtered students on the selected date
    #     if selected_date:
    #         attendance_records = Attendance.objects.filter(student__in=students, date=selected_date)
    #     else:
    #         attendance_records = Attendance.objects.filter(student__in=students)

    return render(request, 'student_attendance_management.html', {
        'classes': classes,
        'sections': sections,
        'a1':a1
        # 'attendance_records': attendance_records
    })

def get_attendance_summary(request):
    
    class_id = request.GET.get('class_id')
    section_id = request.GET.get('section_id')

    students = studentadmission.objects.filter(classs_id=class_id, section_id=section_id)
    attendance_records = Attendance.objects.filter(student__in=students)

    summary = {}

    for record in attendance_records:
        date_str = record.date.strftime("%Y-%m-%d")
        if date_str not in summary:
            summary[date_str] = {'present': 0, 'absent': 0, 'pending': 0}
        
        if record.status == 'Present':
            summary[date_str]['present'] += 1
        elif record.status == 'Absent':
            summary[date_str]['absent'] += 1
        else:
            summary[date_str]['pending'] += 1

    result = [{'date': date, 'present': counts['present'], 'absent': counts['absent'], 'pending': counts['pending']} for date, counts in summary.items()]
    
    return JsonResponse(result, safe=False)


# AJAX view to get sections dynamically based on selected class
def get_sections1(request):
    class_id = request.GET.get('class_id')
    sections = Section.objects.filter(class_assigned_id=class_id).values('id', 'name')
    return JsonResponse(list(sections), safe=False)

def attendence(request):
    try:
        n = TransportInformation.objects.get(custid=request.user)
    except TransportInformation.DoesNotExist:
        n = None

    return render(request,)
    

def std_attendance(request):
    try:
        fm = Teacher.objects.get(custid=request.user)
    except Teacher.DoesNotExist:
        fm = None 

    if fm is not None:
        try:
            headings = teacherdashboardheading.objects.filter(school=fm.school).prefetch_related('teachersubmenu_set')
        except teacherdashboardheading.DoesNotExist:
            headings = None
    else:
        headings = None
    teacher = Teacher.objects.get(custid=request.user)  # Get the logged-in teacher
    attendance_records = None  # Initially no records

    if request.method == "GET" and 'date' in request.GET:
        date_str = request.GET.get('date')

        try:
            selected_date = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else None
        except ValueError:
            selected_date = None

        if selected_date:
            attendance_records = Attendance.objects.filter(teacher=teacher, date=selected_date)

    return render(request, 'std_attendance_manage.html', {
        'attendance_records': attendance_records,'headings':headings,'fm':fm
    })

    

#================================Updates========================================================


import csv
import pandas as pd
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.pdfgen import canvas
import logging
from reportlab.lib.pagesizes import A3, landscape


# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def export_data(request):
    try:
        a1 = SchoolDetails.objects.get(custid=request.user)
    except SchoolDetails.DoesNotExist:
        messages.error(request, "School details not found!")
        return redirect('admin_dashboard')  # Redirect if school is not set up
    file_format = request.GET.get('format')
    selected_fields = request.GET.get('fields', '').split(',')

    # Validate input
    if not file_format or not selected_fields or selected_fields == ['']:
        logger.error("Invalid request: format=%s, fields=%s", file_format, selected_fields)
        return HttpResponse("Invalid request. Please select a format and at least one valid field.", status=400)

    try:
        # Fetch all student records
        students = studentadmission.objects.filter(school=a1)
        logger.debug("Fetched %d students", students.count())

        # Fetch related data
        education_details = {e.stdid_id: e for e in EducationDetail.objects.filter(school=a1)}
        previous_schools = {p.stdid_id: p for p in Previousschooling.objects.filter(school=a1)}
        family_details = {f.stdid_id: f for f in FamilyDetails.objects.filter(school=a1)}
        sibling_docs = {s.stdid_id: s for s in SiblingDocumentSubmission.objects.filter(school=a1)}
        transport_info = {t.stdid_id: t for t in TransportInformation.objects.filter(school=a1)}

        # Combine data
        combined_data = [
            (
                student,
                education_details.get(student.id, None),
                previous_schools.get(student.id, None),
                family_details.get(student.id, None),
                sibling_docs.get(student.id, None),
                transport_info.get(student.id, None),
            )
            for student in students
        ]

        # Define valid fields from all models
        valid_fields = {
            'studentadmission': [field.name for field in studentadmission._meta.fields],
            'education_detail': [field.name for field in EducationDetail._meta.fields],
            'previousschooling': [field.name for field in Previousschooling._meta.fields],
            'family_details': [field.name for field in FamilyDetails._meta.fields],
            'sibling_docs': [field.name for field in SiblingDocumentSubmission._meta.fields],
            'transport_info': [field.name for field in TransportInformation._meta.fields],
        }

        # Filter selected fields to ensure they are valid
        def get_field_value(model_name, field, obj):
            if obj and field in valid_fields[model_name]:
                value = getattr(obj, field, "")
                return str(value) if value is not None else ""
            return ""

        # Prepare data for export
        export_data = []
        headers = selected_fields

        for student, edu, prev, fam, sib, trans in combined_data:
            row = []
            for field in selected_fields:
                if field in valid_fields['studentadmission']:
                    row.append(get_field_value('studentadmission', field, student))
                elif field in valid_fields['education_detail']:
                    row.append(get_field_value('education_detail', field, edu))
                elif field in valid_fields['previousschooling']:
                    row.append(get_field_value('previousschooling', field, prev))
                elif field in valid_fields['family_details']:
                    row.append(get_field_value('family_details', field, fam))
                elif field in valid_fields['sibling_docs']:
                    row.append(get_field_value('sibling_docs', field, sib))
                elif field in valid_fields['transport_info']:
                    row.append(get_field_value('transport_info', field, trans))
                else:
                    row.append("")
            export_data.append(row)

        # Export based on format
        if file_format == 'excel':
            df = pd.DataFrame(export_data, columns=headers)
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="students.xlsx"'
            df.to_excel(response, index=False, engine='openpyxl')
            logger.debug("Excel export successful")
            return response

        elif file_format == 'pdf':
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="students.pdf"'

            doc = SimpleDocTemplate(response, pagesize=landscape(A3))
            elements = []

            # Table Data
            data = [headers] + export_data
            logger.debug("PDF data prepared: %d rows, %d columns", len(data), len(headers))

            # Dynamic column widths with safety check
            total_fields = len(selected_fields)
            col_width = (16.5 * inch) / total_fields if total_fields > 0 else 1 * inch

            table = Table(data, colWidths=[col_width] * total_fields)
            style = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ])
            table.setStyle(style)

            elements.append(table)
            doc.build(elements)
            logger.debug("PDF export successful")
            return response

        logger.error("Invalid format: %s", file_format)
        return HttpResponse("Invalid format", status=400)

    except Exception as e:
        logger.error("Error in export_data for %s: %s", file_format, str(e))
        return HttpResponse(f"Error generating {file_format.upper()}: {str(e)}", status=500)


from django.views.decorators.csrf import csrf_exempt

@csrf_exempt  # To allow AJAX POST requests
def delete_students(request):
    if request.method == "POST":
        student_ids = request.POST.getlist("student_ids[]")  # Get selected student IDs

        if not student_ids:
            return JsonResponse({"error": "No students selected"}, status=400)

        # Delete related data first to avoid integrity errors
        EducationDetail.objects.filter(stdid__in=student_ids, status=0).update(status=1)
        Previousschooling.objects.filter(stdid__in=student_ids,status=0).update(status=1)
        FamilyDetails.objects.filter(stdid__in=student_ids,status=0).update(status=1)
        SiblingDocumentSubmission.objects.filter(stdid__in=student_ids,status=0).update(status=1)
        TransportInformation.objects.filter(stdid__in=student_ids,status=0).update(status=1)
        student_fee_Amount.objects.filter(stdid__in=student_ids,status=0).update(status=1)

        studentadmission.objects.filter(id__in=student_ids,status=0).update(status=1)


        return JsonResponse({"success": True, "message": "Selected students deleted successfully"})

    return JsonResponse({"error": "Invalid request"}, status=400)


def bulkdataedit(request):
    try:
        a1 = SchoolDetails.objects.get(custid=request.user)
    except SchoolDetails.DoesNotExist:
        messages.error(request, "School details not found!")
        return redirect('admin_dashboard')  # Redirect if school is not set up
    search_query = request.GET.get('search', '')  # Get the search term from the URL parameters
    page_number = request.GET.get('page', 1)  # Get the current page number from request

    # Filter student records based on the search query
    if search_query:
        students = studentadmission.objects.filter(
            Q(registrationno__icontains=search_query) | 
            Q(studentname__icontains=search_query) | 
            Q(classs__icontains=search_query)
        )
    else:
        students = studentadmission.objects.filter(school=a1)

    # Paginate the student records
    paginator = Paginator(students, 10)  # Show 10 records per page
    students_page = paginator.get_page(page_number)

    # Fetch related data based on student ID
    education_details = {e.stdid_id: e for e in EducationDetail.objects.filter(school=a1)}
    previous_schools = {p.stdid_id: p for p in Previousschooling.objects.filter(school=a1)}
    family_details = {f.stdid_id: f for f in FamilyDetails.objects.filter(school=a1)}
    sibling_docs = {s.stdid_id: s for s in SiblingDocumentSubmission.objects.filter(school=a1)}
    transport_info = {t.stdid_id: t for t in TransportInformation.objects.filter(school=a1)}

    # Combine data while handling missing values
    combined_data = [
        (
            student,
            education_details.get(student.id, None),
            previous_schools.get(student.id, None),
            family_details.get(student.id, None),
            sibling_docs.get(student.id, None),
            transport_info.get(student.id, None),
        )
        for student in students_page
    ]

    # Check if any student is found
    no_data_found = not students.exists()

    return render(request, "bulk_edit.html", {
        'combined_data': combined_data, 
        'no_data_found': no_data_found,
        'search_query': search_query,
        'students_page': students_page,
        'a1':a1
    })


import json

@csrf_exempt
def update_student_ajax(request):
    if request.method == "POST":
        try:
            data = request.POST
            student_id = data.get("student_id")
            field = data.get("field")
            value = data.get("value")

            print(f"Received AJAX request: student_id={student_id}, field={field}, value={value}")

            student = studentadmission.objects.get(id=student_id)
            if field in ["enqno",
"registrationno",
"studentname",
"classs",
"section",
"amount",
"discounted_amount",
"studenttype",
"gender",
"dateofbirth",
"aadharno",
"house",
"stream",
"emil",
"previousyearattendance",
"mothertongue",
"adoptedchild",
"minority",
"specify",
"nationality",
"mediumofinstruction",
"castecategory",
"optionalsubject",
"offeredsubject",
"penno",
"bloodgroup",
"leftvision",
"rightvision",
"weight",
"height",
"disability",
"sportsactivity",
"admissiondate",
"bankname",
"branchname",
"accountno",
"ifsccode","mbno"]:
                setattr(student, field, value)
                student.save()
                print(f"Updated {field} in studentadmission model: {value}")

            elif field in ["father_name",
"mother_name",
"guardian_name",
"father_email",
"mother_email",
"guardian_email",
"father_nationality",
"mother_nationality",
"guardian_nationality",
"father_occupation",
"mother_occupation",
"guardian_occupation",
"father_department",
"mother_department",
"guardian_department",
"father_designation",
"mother_designation",
"guardian_designation",
"father_name_of_office",
"mother_name_of_office",
"guardian_name_of_office",
"father_office_address",
"mother_office_address",
"guardian_office_address",
"father_office_contact_no",
"mother_office_contact_no",
"guardian_office_contact_no",
"father_aadhar_no",
"mother_aadhar_no",
"guardian_aadhar_no",
"father_pan_no",
"mother_pan_no",
"guardian_pan_no",
"father_annual_income",
"mother_annual_income",
"guardian_annual_income",
"father_mobile",
"mother_mobile",
"guardian_mobile",
"father_mobile2",
"mother_mobile2",
"guardian_mobile2",
"father_religion",
"mother_religion",
"guardian_religion",
"father_caste",
"mother_caste",
"guardian_caste",
"father_marital_status",
"mother_marital_status",
"guardian_marital_status",
"guardian_relation",
"guardian_address",
"guardian_whatsapp",
"guardian_place",
"guardian_area",
"guardian_location",
"guardian_state",
"guardian_city",
"corres_address",
"corres_mobile_no",
"corres_whatsapp",
"corres_place",
"corres_area",
"corres_location",
"corres_state",
"corres_city"
]:
                family = FamilyDetails.objects.filter(stdid=student).first()
                if family:
                    setattr(family, field, value)
                    family.save()
                    print(f"Updated {field} in FamilyDetails model: {value}")

            elif field in ["qualificationg1","qualificationm1","qualificationf1"]:
                education = EducationDetail.objects.filter(stdid=student).first()
                if education:
                    setattr(education, field, value)
                    education.save()
                    print(f"Updated qualification in EducationDetail model: {value}")
            
            elif field in ["name1",
"age1",
"gender1",
"school1",
"class1",
"name2",
"age2",
"gender2",
"school2",
"class2",
"admission_form",
"school_leaving_certificate",
"bonafide_certificate",
"birth_certificate"
]:
                education1 = SiblingDocumentSubmission.objects.filter(stdid=student).first()
                if education1:
                    setattr(education1, field, value)
                    education1.save()
                    print(f"Updated qualification in SiblingDocumentSubmission model: {value}")

            elif field in ["transport_available",
"bus_no",
"driver_name",
"mobile",
"route",
"stoppage",
"fee",
"pick_up",
"drop_off",
"fee_category",
"fee_type"
]:
                transport = TransportInformation.objects.filter(stdid=student).first()
                if transport:
                    setattr(transport, field, value)
                    transport.save()
                    print(f"Updated fee_type in TransportInformation model: {value}")

            return JsonResponse({"status": "success"})

        except studentadmission.DoesNotExist:
            print("Error: Student not found.")
            return JsonResponse({"status": "error", "message": "Student not found."})
        except Exception as e:
            print(f"Error: {str(e)}")
            return JsonResponse({"status": "error", "message": str(e)})

    return JsonResponse({"status": "error", "message": "Invalid request."})


def deleted_students(request):
    try:
        a1 = SchoolDetails.objects.get(custid=request.user)
    except SchoolDetails.DoesNotExist:
        messages.error(request, "School details not found!")
        return redirect('admin_dashboard')  # Redirect if school is not set up
    
    search_query = request.GET.get('search', '')  # Get the search term from the URL parameters
    page_number = request.GET.get('page', 1)  # Get the current page number from request

    # Filter student records based on the search query
    if search_query:
        students = studentadmission.objects.filter(
            Q(registrationno__icontains=search_query) | 
            Q(studentname__icontains=search_query) | 
            Q(classs__icontains=search_query)
        )
    else:
        students = studentadmission.objects.filter(school=a1)

    # Paginate the student records
    paginator = Paginator(students, 10)  # Show 10 records per page
    students_page = paginator.get_page(page_number)

    # Fetch related data based on student ID
    education_details = {e.stdid_id: e for e in EducationDetail.objects.all()}
    previous_schools = {p.stdid_id: p for p in Previousschooling.objects.all()}
    family_details = {f.stdid_id: f for f in FamilyDetails.objects.all()}
    sibling_docs = {s.stdid_id: s for s in SiblingDocumentSubmission.objects.all()}
    transport_info = {t.stdid_id: t for t in TransportInformation.objects.all()}

    # Combine data while handling missing values
    combined_data = [
        (
            student,
            education_details.get(student.id, None),
            previous_schools.get(student.id, None),
            family_details.get(student.id, None),
            sibling_docs.get(student.id, None),
            transport_info.get(student.id, None),
        )
        for student in students_page
    ]

    # Check if any student is found
    no_data_found = not students.exists()

    return render(request, "deleted_student_list.html", {
        'combined_data': combined_data, 
        'no_data_found': no_data_found, 
        'search_query': search_query,
        'students_page': students_page,
        'a1':a1  
    })

    
@csrf_exempt  # To allow AJAX POST requests
def restore_students(request):
    if request.method == "POST":
        student_ids = request.POST.getlist("student_ids[]")  # Get selected student IDs

        if not student_ids:
            return JsonResponse({"error": "No students selected"}, status=400)

        studentadmission.objects.filter(id__in=student_ids,status=1).update(status=0)


        return JsonResponse({"success": True, "message": "Selected students deleted successfully"})

    return JsonResponse({"error": "Invalid request"}, status=400)



# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def export_teachers_data(request):
    try:
        a1 = SchoolDetails.objects.get(custid=request.user)
    except SchoolDetails.DoesNotExist:
        messages.error(request, "School details not found!")
        return redirect('admin_dashboard')  # Redirect if school is not set up
    
    file_format = request.GET.get('format')
    selected_fields = request.GET.get('fields', '').split(',')

    # Validate input
    if not file_format or not selected_fields or selected_fields == ['']:
        logger.error("Invalid request: format=%s, fields=%s", file_format, selected_fields)
        return HttpResponse("Invalid request. Please select a format and at least one valid field.", status=400)

    try:
        # Fetch all teacher records
        teachers = Teacher.objects.filter(school=a1)
        logger.debug("Fetched %d teachers", teachers.count())

        # Define valid fields from the Teacher model
        valid_fields = {
            'teacher': [field.name for field in Teacher._meta.fields],
            # Add related models here if applicable, e.g.:
            # 'education_detail': [field.name for field in EducationDetail._meta.fields],
        }

        # Filter selected fields to ensure they are valid
        def get_field_value(model_name, field, obj):
            if obj and field in valid_fields[model_name]:
                value = getattr(obj, field, "")
                return str(value) if value is not None else ""
            return ""

        # Prepare data for export
        export_data = []
        headers = selected_fields

        for teacher in teachers:
            row = []
            for field in selected_fields:
                if field in valid_fields['teacher']:
                    row.append(get_field_value('teacher', field, teacher))
                else:
                    row.append("")  # Default for invalid fields
            export_data.append(row)

        # Export based on format
        if file_format == 'excel':
            df = pd.DataFrame(export_data, columns=headers)
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="teachers.xlsx"'
            df.to_excel(response, index=False, engine='openpyxl')
            logger.debug("Excel export successful")
            return response

        elif file_format == 'pdf':
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="teachers.pdf"'

            doc = SimpleDocTemplate(response, pagesize=landscape(A3))
            elements = []

            # Table Data
            data = [headers] + export_data
            logger.debug("PDF data prepared: %d rows, %d columns", len(data), len(headers))

            # Dynamic column widths with safety check
            total_fields = len(selected_fields)
            col_width = (16.5 * inch) / total_fields if total_fields > 0 else 1 * inch

            table = Table(data, colWidths=[col_width] * total_fields)
            style = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ])
            table.setStyle(style)

            elements.append(table)
            doc.build(elements)
            logger.debug("PDF export successful")
            return response

        logger.error("Invalid format: %s", file_format)
        return HttpResponse("Invalid format", status=400)

    except Exception as e:
        logger.error("Error in export_teachers_data for %s: %s", file_format, str(e))
        return HttpResponse(f"Error generating {file_format.upper()}: {str(e)}", status=500)




def bulk_insert_teacher(request):
    if request.method == 'POST' and request.FILES['excel_file']:
        excel_file = request.FILES['excel_file']
        df = pd.read_excel(excel_file)

        for index, row in df.iterrows():
            try:
                # Create CustomUser
                user = CustomUser.objects.create(
                    username=row['username'],
                    email=row['email'],
                    password=make_password(row['password']),
                    role=row['role']
                )

                # Create studentadmission
                student = Teacher.objects.create(
                    
                    first_name=row['first_name'],
                    last_name=row['last_name'],
                    email=row['email'],
                    phone=row['phone'],
                    date_of_birth=row['date_of_birth'],
                    custid=user
                )

               
            except Exception as e:
                return JsonResponse({"error": f"Error processing row {index}: {str(e)}"}, status=400)

        return JsonResponse({"message": "Bulk data insertion successful."})


@csrf_exempt  
def delete_teacher(request):
    if request.method == "POST":
        student_ids = request.POST.getlist("student_ids[]")  # Get selected student IDs

        if not student_ids:
            return JsonResponse({"error": "No students selected"}, status=400)

        Teacher.objects.filter(id__in=student_ids,status=0).update(status=1)


        return JsonResponse({"success": True, "message": "Selected students deleted successfully"})

    return JsonResponse({"error": "Invalid request"}, status=400)



def deleted_teachers(request):
    try:
        a1 = SchoolDetails.objects.get(custid=request.user)
    except SchoolDetails.DoesNotExist:
        messages.error(request, "School details not found!")
        return redirect('admin_dashboard')  # Redirect if school is not set up
    search_query = request.GET.get('search', '').strip()
    teachers = Teacher.objects.filter(school=a1)

    # Apply search filter
    if search_query:
        teachers = teachers.filter(Q(first_name__icontains=search_query) | Q(subjects__icontains=search_query))

    # Paginate results
    paginator = Paginator(teachers, 500)  # Show 5 teachers per page
    page_number = request.GET.get('page')
    teachers_page = paginator.get_page(page_number)

    context = {
        'tea': teachers_page,
        'search_query': search_query,
        'students_page': teachers_page,  # Used for pagination
        'no_data_found': search_query and not teachers.exists(),
        'a1':a1
    }
    
    return render(request, "deleted_teacher_list.html", context)



@csrf_exempt  # To allow AJAX POST requests
def restore_teachers(request):
    try:
        a1 = SchoolDetails.objects.get(custid=request.user)
    except SchoolDetails.DoesNotExist:
        messages.error(request, "School details not found!")
        return redirect('admin_dashboard')  # Redirect if school is not set up
    if request.method == "POST":
        student_ids = request.POST.getlist("student_ids[]")  # Get selected student IDs

        if not student_ids:
            return JsonResponse({"error": "No students selected"}, status=400)

        Teacher.objects.filter(id__in=student_ids,status=1,school=a1).update(status=0)


        return JsonResponse({"success": True, "message": "Selected students deleted successfully"})

    return JsonResponse({"error": "Invalid request"}, status=400)






def family(request):
    search_query = request.GET.get('search', '')  
    page_number = request.GET.get('page', 1)  

    # Filter student records based on the search query
    if search_query:
        students = studentadmission.objects.filter(
            Q(registrationno__icontains=search_query) | 
            Q(studentname__icontains=search_query) | 
            Q(classs__icontains=search_query)
        )
    else:
        students = studentadmission.objects.all()

    # Paginate the student records
    paginator = Paginator(students, 10)  # Show 10 records per page
    students_page = paginator.get_page(page_number)

    # Fetch related data based on student ID
    education_details = {e.stdid_id: e for e in EducationDetail.objects.all()}
    previous_schools = {p.stdid_id: p for p in Previousschooling.objects.all()}
    family_details = {f.stdid_id: f for f in FamilyDetails.objects.all()}
    sibling_docs = {s.stdid_id: s for s in SiblingDocumentSubmission.objects.all()}
    transport_info = {t.stdid_id: t for t in TransportInformation.objects.all()}
    fee = {t.stdid_id: t for t in student_fee_Amount.objects.all()}

    # Combine data while handling missing values
    combined_data = [
        (
            student,
            education_details.get(student.id, None),
            previous_schools.get(student.id, None),
            family_details.get(student.id, None),
            sibling_docs.get(student.id, None),
            transport_info.get(student.id, None),
            fee.get(student.id, None),
        )
        for student in students_page
    ]

    # Check if any student is found
    no_data_found = not students.exists()

    return render(request, "familydetails.html", {
        'combined_data': combined_data, 
        'no_data_found': no_data_found, 
        'search_query': search_query,
        'students_page': students_page,  # Pass the paginated object to the template
    })


def teacher_marks_feeding(request):
    
    try:
        fm = Teacher.objects.get(custid=request.user)
    except Teacher.DoesNotExist:
        fm = None 

    if fm is not None:
        try:
            headings = teacherdashboardheading.objects.filter(school=fm.school).prefetch_related('teachersubmenu_set')
        except teacherdashboardheading.DoesNotExist:
            headings = None
    else:
        headings = None
    try:
        t = Teacher.objects.get(custid=request.user)
        assigned_classes = t.assigned_classes1.all()
        assigned_sections = t.assigned_sections1.all()
        fn = exam.objects.filter(school=t.school)
        selected_class = request.GET.get('class')
        selected_section = request.GET.get('section')

        students = studentadmission.objects.filter(
            classs__in=assigned_classes, section__in=assigned_sections
        )

        # Filter sections by selected class
        filtered_sections = assigned_sections.filter(class_assigned__id=selected_class) if selected_class else []

        if selected_class:
            students = students.filter(classs__id=selected_class)

        if selected_section:
            students = students.filter(section__id=selected_section)

        # Filter subjects based on the selected class
        assigned_subjects = Subject.objects.filter(class_assigned__id=selected_class) if selected_class else []

        # Handle marks submission
        if request.method == "POST":
            exam_id = request.POST.get("exam_type")  # Get selected exam ID
            selected_exam = exam.objects.get(id=exam_id) if exam_id else None

            if selected_exam:
                for student in students:
                    for subject in assigned_subjects:
                        marks_key = f"marks_{student.id}_{subject.id}"
                        marks_value = request.POST.get(marks_key)

                        if marks_value:
                            # Save marks with exam association
                            StudentMarks1.objects.update_or_create(
                                student=student,
                                subject=subject,
                                teacher=t,
                                exam=selected_exam,  # Include exam association
                                defaults={'marks': int(marks_value)},
                                school=t.school,
                            )

                messages.success(request, "Marks saved successfully!")
                return redirect("dashboard")
            else:
                messages.error(request, "Please select an exam type!")

    except Teacher.DoesNotExist:
        t = None
        students = []
        assigned_classes = []
        assigned_sections = []
        assigned_subjects = []
        filtered_sections = []

    context = {
        'user': request.user,
        't': t,
        'fn': fn,
        'students': students,
        'assigned_classes': assigned_classes,
        'assigned_sections': assigned_sections,
        "filtered_sections": filtered_sections,
        "assigned_subjects": assigned_subjects,
        'headings':headings,
        'fm':fm,
    }
    
    return render(request, "teacher_marks_feeding.html", context)



from django.db.models import Sum, Count, Min
from django.contrib import messages
from django.http import Http404

def view_student_marks(request):
    """ View to display student marks with filters and edit links """
    try:
        fm = Teacher.objects.get(custid=request.user)
    except Teacher.DoesNotExist:
        fm = None 

    if fm is not None:
        try:
            headings = teacherdashboardheading.objects.filter(school=fm.school).prefetch_related('teachersubmenu_set')
        except teacherdashboardheading.DoesNotExist:
            headings = None
    else:
        headings = None
    try:
        # Get the logged-in teacher
        teacher = Teacher.objects.get(custid=request.user)

        # Fetch unique classes, sections, and exams
        classes = StudentMarks1.objects.filter(teacher=teacher).values(
            'student__classs__id', 'student__classs__name'
        ).distinct()

        sections = StudentMarks1.objects.filter(teacher=teacher).values(
            'student__section__id', 'student__section__name'
        ).distinct()

        exams = StudentMarks1.objects.filter(teacher=teacher).values(
            'exam__id', 'exam__examname'
        ).distinct()

        # Get filter values from GET request
        selected_class = request.GET.get('class')
        selected_section = request.GET.get('section')
        selected_exam = request.GET.get('exam')

        # Filter marks based on the selected filters
        marks_query = StudentMarks1.objects.select_related(
            'student__classs', 
            'student__section', 
            'subject', 
            'exam'
        ).filter(teacher=teacher)

        if selected_class:
            marks_query = marks_query.filter(student__classs_id=selected_class)

        if selected_section:
            marks_query = marks_query.filter(student__section_id=selected_section)

        if selected_exam:
            marks_query = marks_query.filter(exam_id=selected_exam)

        # Aggregate marks by student and exam
        marks = (
            marks_query.values(
                'student__id',
                'student__studentname',
                'student__mbno',
                'student__registrationno',
                'student__classs__name',
                'student__section__name',
                'exam__examname',
                'exam__id',
            )
            .annotate(
                total_marks=Count('subject') * 100,   # Assuming each subject has 100 max marks
                obtained_marks=Sum('marks'),
                mark_id=Min('id')  # Retrieve the first mark ID for the edit link
            )
            .order_by('student__id', 'exam__id')
        )

        # Calculate percentage
        for mark in marks:
            total = mark['total_marks']
            obtained = mark['obtained_marks']
            mark['percentage'] = round((obtained / total) * 100, 2) if total > 0 else 0

    except Teacher.DoesNotExist:
        messages.error(request, "Teacher not found.")
        marks, classes, sections, exams = [], [], [], []

    # Pass context to template
    context = {
        'marks': marks,
        'classes': classes,
        'sections': sections,
        'exams': exams,
        'selected_class': selected_class,
        'selected_section': selected_section,
        'selected_exam': selected_exam,
        'headings':headings,
        'fm':fm
    }

    return render(request, "view_student_marks.html", context)


from django.db import transaction

def edit_student_marks(request, student_id, exam_id):
    try:
        fm = Teacher.objects.get(custid=request.user)
    except Teacher.DoesNotExist:
        fm = None 

    if fm is not None:
        try:
            headings = teacherdashboardheading.objects.filter(school=fm.school).prefetch_related('teachersubmenu_set')
        except teacherdashboardheading.DoesNotExist:
            headings = None
    else:
        headings = None
    
    """View to edit all subjects' marks for a student in a specific exam"""

    # Retrieve all marks for the selected student and exam
    marks = StudentMarks1.objects.filter(student_id=student_id, exam_id=exam_id).select_related('subject')

    if not marks.exists():
        messages.error(request, "No marks found for this student and exam.")
        return redirect('view_student_marks')

    if request.method == "POST":
        # Save all subjects' marks in a single transaction
        with transaction.atomic():
            for mark in marks:
                mark_value = request.POST.get(f'mark_{mark.id}')
                if mark_value.isdigit():  # Validate that the value is a digit
                    mark.marks = int(mark_value)
                    mark.save()
            messages.success(request, "Marks updated successfully!")
            return redirect('view_student_marks')

    context = {
        'marks': marks,
        'student_name': marks[0].student.studentname,
        'exam_name': marks[0].exam.examname,
        'fm':fm,
        'headings':headings
    }

    return render(request, "edit_student_marks.html", context)

def view_report_card(request, student_id, exam_id):
    """View to display the report card for a student in a particular exam"""
    
    # Get student and exam details
    student = get_object_or_404(studentadmission, id=student_id)
    exam_obj = get_object_or_404(exam, id=exam_id)

    # Fetch all subjects and marks for the student in the selected exam
    marks = StudentMarks1.objects.filter(
        student=student, 
        exam=exam_obj
    ).select_related('subject')

    # Fetch extra subject marks
    extra_subjects = ExtraSubjectMarks.objects.filter(
        student=student, 
        exam=exam_obj
    )

    # Fetch individual marks from SubjectMarksDetail
    marks_details = SubjectMarksDetail.objects.filter(
        student=student,
        exam=exam_obj
    ).select_related('subject')

     # Retrieve Co-Scholastic grading scale
    co_scholastic_grades = CoScholasticGrade.objects.all()

    # Retrieve discipline grade for the student and exam
    discipline_grade = DisciplineGrade.objects.filter(student=student, exam=exam_obj).first()

    # Retrieve remarks
    remark = Remark.objects.filter(student=student, exam=exam_obj).first()

    # Retrieve signature and report date
    signature = ReportCardSignature.objects.filter(student=student, exam=exam_obj).first()


    # Organize marks into individual categories
    report_data = []
    total_obtained = 0
    total_max_marks = 0

    for index, mark in enumerate(marks_details, start=1):
        total = mark.total
        total_obtained += total
        total_max_marks += 100

    

        # Grade Calculation
        if total >= 91:
            grade = "A1"
        elif total >= 81:
            grade = "A2"
        elif total >= 71:
            grade = "B1"
        elif total >= 61:
            grade = "B2"
        elif total >= 51:
            grade = "C1"
        elif total >= 41:
            grade = "C2"
        else:
            grade = "D"

        report_data.append({
            'sno': index,
            'subject': mark.subject.name,
            'pa': mark.pa,
            'se': mark.se,
            'ma': mark.ma,
            'nb': mark.nb,
            'term': mark.term,
            'total': mark.total,
            'grade': grade,
        })

    # Calculate overall percentage
    percentage = round((total_obtained / total_max_marks) * 100, 2) if total_max_marks > 0 else 0

    try:
        fm = Teacher.objects.get(custid=request.user)
    except Teacher.DoesNotExist:
        fm = None 

    if fm is not None:
        try:
            headings = teacherdashboardheading.objects.filter(school=fm.school).prefetch_related('teachersubmenu_set')
        except teacherdashboardheading.DoesNotExist:
            headings = None
    else:
        headings = None
    # Filter photo based on user school, class, section, and exam
    class_photo = ClassPhoto1.objects.filter(
        school=fm.school,
        class_name=student.classs,
        section=student.section,
        exam=exam_obj
    ).first()

    context = {
        'student': student,
        'exam': exam_obj,
        'report_data': report_data,
        'total_obtained': total_obtained,
        'total_max_marks': total_max_marks,
        'percentage': percentage,
        'extra_subjects': extra_subjects,
        'co_scholastic_grades': co_scholastic_grades,
        'discipline_grade': discipline_grade,
        'remark': remark,
        'signature': signature,
        'class_photo':class_photo,
        'headings':headings,
    }

    return render(request, 'view_report_card.html', context)


from django.template.loader import get_template
from xhtml2pdf import pisa

def download_report_card(request, student_id, exam_id):
    """Generate and download the report card as PDF"""

    student = get_object_or_404(studentadmission, id=student_id)
    exam_obj = get_object_or_404(exam, id=exam_id)

    # Fetch the marks for the student in the selected exam
    marks = StudentMarks1.objects.filter(student=student, exam=exam_obj).select_related('subject')

    # Calculate total and obtained marks
    total_marks = marks.count() * 100  # Assuming each subject has 100 marks
    obtained_marks = marks.aggregate(total=Sum('marks'))['total'] or 0
    percentage = round((obtained_marks / total_marks) * 100, 2) if total_marks > 0 else 0

    # Prepare context for the template
    context = {
        'student': student,
        'exam': exam_obj,
        'marks': marks,
        'total_marks': total_marks,
        'obtained_marks': obtained_marks,
        'percentage': percentage,
    }

    # Load the template and render it with the context
    template = get_template('report_card_pdf_template.html')
    html = template.render(context)

    # Generate PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=ReportCard_{student.studentname}_{exam_obj.examname}.pdf'

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error generating PDF', status=500)

    return response

def delete_student_marks(request, mark_id):
    """View to delete student marks"""
    
    mark = get_object_or_404(StudentMarks1, id=mark_id)

    if request.method == "POST":  # Ensure only POST requests delete the mark
        mark.delete()
        messages.success(request, "Student marks deleted successfully.")
        return redirect('view_student_marks')  # Redirect back to the marks page

    messages.error(request, "Invalid request.")
    return redirect('view_student_marks')    


from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import studentadmission, exam, ExtraSubjectMarks, AssignedClass, Teacher

def insert_extra_subject_marks(request):
    """Insert multiple extra subject marks for a student"""
    try:
        fm = Teacher.objects.get(custid=request.user)
    except Teacher.DoesNotExist:
        fm = None 

    if fm is not None:
        try:
            headings = teacherdashboardheading.objects.filter(school=fm.school).prefetch_related('teachersubmenu_set')
        except teacherdashboardheading.DoesNotExist:
            headings = None
    else:
        headings = None
    teacher = Teacher.objects.get(custid=request.user)


    if request.method == "POST":
        student_id = request.POST.get('student')
        exam_id = request.POST.get('exam')
        
        # Fetch student and exam objects
        student = studentadmission.objects.get(id=student_id)
        exam_obj = exam.objects.get(id=exam_id)


        subjects = request.POST.getlist('subject[]')
        pa_marks = request.POST.getlist('pa[]')
        se_marks = request.POST.getlist('se[]')
        ma_marks = request.POST.getlist('ma[]')
        nb_marks = request.POST.getlist('nb[]')

        for subject_name, pa, se, ma, nb in zip(subjects, pa_marks, se_marks, ma_marks, nb_marks):
            subject_obj = get_object_or_404(Subject, name=subject_name, class_assigned=student.classs)

            # Fetch the existing term marks from StudentMarks1
            term_marks = StudentMarks1.objects.filter(
                student=student, subject=subject_obj, exam=exam_obj
            ).first()

            term_score = term_marks.marks if term_marks else 0  # Use existing term marks or default to 0

            # Save or update SubjectMarksDetail
            subject_marks, created = SubjectMarksDetail.objects.get_or_create(
                student=student,
                subject=subject_obj,
                exam=exam_obj,
                defaults={
                    'pa': float(pa) if pa else 0,
                    'se': float(se) if se else 0,
                    'ma': float(ma) if ma else 0,
                    'nb': float(nb) if nb else 0,
                    'term': term_score
                }
            )

            # If record already exists, update marks
            if not created:
                subject_marks.pa = float(pa) if pa else 0
                subject_marks.se = float(se) if se else 0
                subject_marks.ma = float(ma) if ma else 0
                subject_marks.nb = float(nb) if nb else 0
                subject_marks.term = term_score

            # Automatically calculate total
            subject_marks.total = round(subject_marks.pa + subject_marks.se + subject_marks.ma + subject_marks.nb + subject_marks.term)
            subject_marks.save()


        subjects = request.POST.getlist('subject[]')
        grades = request.POST.getlist('grade[]')
        # marks = request.POST.getlist('marks[]')

        for subject, grade in zip(subjects, grades):
            if subject and grade:
                ExtraSubjectMarks.objects.create(
                    student=student,
                    exam=exam_obj,
                    subject=subject,
                    grade=grade,
                    # marks=mark
                )

        # Handling Co-Scholastic Grades
        co_grades = request.POST.getlist('co_grade[]')
        co_points = request.POST.getlist('co_point[]')


        for grade, point in zip(co_grades, co_points):
            if grade and point:
                CoScholasticGrade.objects.create(grade=grade, grade_point=point)        

        # Handling Discipline Grade
        discipline_grade = request.POST.get('discipline_grade')
        DisciplineGrade.objects.update_or_create(
            student=student, exam=exam_obj,
            defaults={'grade': discipline_grade}
        )

        # Handling Remarks
        remark_text = request.POST.get('remark')
        Remark.objects.update_or_create(
            student=student, exam=exam_obj,
            defaults={'remark': remark_text}
        )

        # Handling Signatures
        teacher_signature = request.POST.get('teacher_signature')
        report_date = now()

        ReportCardSignature.objects.update_or_create(
            student=student, exam=exam_obj,
            defaults={'teacher_signature': teacher_signature, 'report_date': report_date}
        )        

        messages.success(request, "Extra subject marks saved successfully!")
        return redirect('insert_extra_subject_marks')

    # Retrieve students assigned to the logged-in teacher
    assigned_classes = AssignedClass.objects.filter(teacher=teacher)

    # Filter students correctly
    students = studentadmission.objects.filter(
        section__in=assigned_classes.values('section'),
        classs__in=assigned_classes.values('class_assigned')
    ).distinct()

    exams = exam.objects.all()

    context = {
        'students': students,
        'exams': exams,
        'headings':headings,
        'fm':fm
    }

    return render(request, 'insert_extra_subject_marks.html', context)

def get_subjects_and_term_marks(request):
    """Fetch subjects and term marks for a student"""
    student_id = request.GET.get('student_id')
    exam_id = request.GET.get('exam_id')

    if student_id and exam_id:
        student = get_object_or_404(studentadmission, id=student_id)
        exam_obj = get_object_or_404(exam, id=exam_id)

        subjects = Subject.objects.filter(class_assigned=student.classs)
        subjects_with_marks = []

        for subject in subjects:
            # Get the existing term marks if they exist
            term_marks = StudentMarks1.objects.filter(
                student=student, subject=subject, exam=exam_obj
            ).first()

            subjects_with_marks.append({
                "name": subject.name,
                "term_marks": term_marks.marks if term_marks else "N/A"
            })

        return JsonResponse(subjects_with_marks, safe=False)

    return JsonResponse([], safe=False)






def teacher_profile(request):
    try:
        t = Teacher.objects.get(custid=request.user)
        assigned_classes = t.assigned_classes1.all()
        assigned_sections = t.assigned_sections1.all()
        
        selected_class = request.GET.get('class')
        selected_section = request.GET.get('section')

        students = studentadmission.objects.filter(
            classs__in=assigned_classes, section__in=assigned_sections
        )

        filtered_sections = assigned_sections.filter(class_assigned__id=selected_class) if selected_class else []

        if selected_class:
            students = students.filter(classs__id=selected_class)

        if selected_section:
            students = students.filter(section__id=selected_section)

        # Filter subjects based on the selected class
        assigned_subjects = Subject.objects.filter(class_assigned__id=selected_class) if selected_class else []

    except Teacher.DoesNotExist:
        t = None
        students = []
        assigned_classes = []
        assigned_sections = []
        assigned_subjects = []
        filtered_sections = []

    context = {
        'user': request.user,
        't':t,
        'students': students, 
        'assigned_classes': assigned_classes,
        'assigned_sections': assigned_sections,
        "filtered_sections": filtered_sections,
        "assigned_subjects" : assigned_subjects,
        
    }    
    return render(request,"teacher_profile.html", context)  


def view_marks_list(request):
    try:
        i = studentadmission.objects.get(custid=request.user)
    except studentadmission.DoesNotExist:
        i = None
    try:
        # Fetch the current student's admission details
        student = studentadmission.objects.get(custid=request.user)
        student_class = student.classs
        
        # Get all exams related to the student's class
        exams = exam.objects.all().order_by('examname')

        # Get the selected exam ID from the GET request
        selected_exam_id = request.GET.get('exam_id')

        # Fetch subjects related to the student's class
        subjects = Subject.objects.filter(class_assigned=student_class)

        # Filter marks based on the selected exam (if provided)
        if selected_exam_id:
            marks = StudentMarks1.objects.filter(student=student, exam_id=selected_exam_id)
        else:
            marks = StudentMarks1.objects.filter(student=student)

    except studentadmission.DoesNotExist:
        student = None
        exams = []
        subjects = []
        marks = []

    context = {
        'marks2': marks,
        'subjects': subjects,
        'exams': exams,
        'selected_exam_id': selected_exam_id,
        'i':i
    }
    return render(request, "view_marks_list.html", context)
  

    #===================================WEBSITE========================================================

    
def home(request):
    return render(request, 'ff/index.html')

def about(request):
    return render(request, 'ff/about.html')

def classes(request):
    return render(request, 'ff/classes.html')

def facility(request):
    return render(request, 'ff/facility.html')

def team(request):
    return render(request, 'ff/team.html')

def become_teacher(request):
    return render(request, 'ff/call-to-action.html')

def appointment(request):
    return render(request, 'ff/appointment.html')

def testimonial(request):
    return render(request, 'ff/testimonial.html')

def error_404(request):
    return render(request, 'ff/404.html')

def contact(request):
    return render(request, 'ff/contact.html')

def student(request):
    return render(request, 'ff/student.html')

def teacher(request):
    return render(request, 'ff/teacher.html')

#======================================================================


def student_view_profile(request):
    return render(request,"student_view_profile.html")

from django.shortcuts import render
from django.http import JsonResponse
from itertools import groupby
from django.db.models import Q

def admin_view_student_marks(request):
    try:
        a1 = SchoolDetails.objects.get(custid=request.user)
    except SchoolDetails.DoesNotExist:
        a1 = None 
    # Fetch distinct classes and exams
    classes = Class.objects.filter(school=a1).order_by('name').distinct()
    exams = exam.objects.filter(school=a1).order_by('examname').distinct()

    # Get filter values from the request
    selected_class = request.GET.get('class')
    selected_section = request.GET.get('section')
    selected_exam = request.GET.get('exam')

    # Fetch marks data with filters
    total_marks = StudentMarks1.objects.filter(school=a1).select_related(
        'student__classs', 'student__section', 'subject', 'teacher'
    ).prefetch_related('exam').order_by(
        'student__studentname', 'student__classs__name', 'student__section__name', 'exam__examname'
    )

    # Apply filters
    if selected_class:
        total_marks = total_marks.filter(student__classs__id=selected_class)
    
    if selected_section:
        total_marks = total_marks.filter(student__section__id=selected_section)

    if selected_exam:
        total_marks = total_marks.filter(exam__id=selected_exam)

    # Group the filtered data
    grouped_data = {}
    for key, group in groupby(total_marks, key=lambda x: (
        x.student.studentname,
        x.student.classs.name,
        x.student.section.name,
        getattr(x.exam, 'examname', 'No Exam')
    )):
        grouped_data[key] = list(group)

    # Fetch sections dynamically based on the selected class
    sections = Section.objects.filter(class_assigned_id=selected_class).distinct() if selected_class else Section.objects.none()

    # Render context
    context = {
        'grouped_data': grouped_data,
        'classes': classes,
        'sections': sections,
        'exams': exams,
        'selected_class': selected_class,
        'selected_section': selected_section,
        'selected_exam': selected_exam,'a1':a1
    }

    return render(request, "admin_view_student_marks.html", context)


from django.http import JsonResponse
from .models import Section

def get_sections2(request):
    """
    AJAX request to get sections by class ID.
    """
    class_id = request.GET.get('class_id')

    if class_id:
        sections = Section.objects.filter(class_assigned_id=class_id).values('id', 'name')
    else:
        sections = []

    return JsonResponse({'sections': list(sections)})



from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ContactMessage

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if name and email and message:  
            ContactMessage.objects.create(name=name, email=email, subject=subject, message=message)
            messages.success(request, "Your message has been sent successfully!")
            return redirect('/')

    return render(request, "ff/contact.html")



from django.contrib import messages

def student_leave_request(request):
    try:
        i = studentadmission.objects.get(custid=request.user)
    except studentadmission.DoesNotExist:
        i = None
    if request.method == "POST":
        subject = request.POST.get("subject")
        from_date = request.POST.get("from_date")
        to_date = request.POST.get("to_date")
        purpose = request.POST.get("purpose")

        # Get the logged-in student
        student = request.user

        # Fetch student details
        student_details = studentadmission.objects.get(custid=student)

        # Find the assigned class teacher
        assigned_class = AssignedClass.objects.filter(
            class_assigned=student_details.classs, 
            section=student_details.section
        ).first()

        if not assigned_class:
            messages.error(request, "No class teacher assigned to your section.")
            return redirect("student_dashboard")

        teacher = assigned_class.teacher

        # Create the leave request
        leave_request = LeaveRequest.objects.create(
            student=student,
            teacher=teacher,
            subject=subject,
            from_date=from_date,
            to_date=to_date,
            purpose=purpose,
            class_assigned=student_details.classs,
            section_assigned=student_details.section
        )

        # Create notification for the teacher
        Notification.objects.create(
            user=teacher.custid,
            message=f"New leave request from {student.username}."
        )

        messages.success(request, "Leave request submitted successfully.")
        return redirect("dashboard")

    return render(request, "student_leave_request.html",{'i':i})


def manage_leave_requests(request):
    # Get the assigned class and section of the teacher
    assigned_classes = AssignedClass.objects.filter(teacher__custid=request.user)
    try:
        fm = Teacher.objects.get(custid=request.user)
    except Teacher.DoesNotExist:
        fm = None 

    if fm is not None:
        try:
            headings = teacherdashboardheading.objects.filter(school=fm.school).prefetch_related('teachersubmenu_set')
        except teacherdashboardheading.DoesNotExist:
            headings = None
    else:
        headings = None

    # Fetch all leave requests for the assigned classes/sections, sorted by creation date (newest first)
    leave_requests = LeaveRequest.objects.filter(
        class_assigned__in=[ac.class_assigned for ac in assigned_classes],
        teacher__custid=request.user
    ).order_by('-created_at')  # Sort by newest first

    # Pagination logic (10 items per page)
    paginator = Paginator(leave_requests, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Fetch notifications
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')[:5]

    context = {
        "page_obj": page_obj,
        "notifications": notifications,
        'headings':headings,
        'fm':fm
    }
    return render(request, "view_leave_requests.html", context)

def accept_leave(request, leave_id):
    leave = get_object_or_404(LeaveRequest, id=leave_id)
    
    # Update the leave status to 'approved'
    leave.status = 'approved'
    leave.save()

    # Send notification to the student
    Notification.objects.create(
        user=leave.student,
        message=f"Your leave request for {leave.subject} has been approved."
    )

    messages.success(request, "Leave request approved successfully.")
    return redirect('dashboard')


def reject_leave(request, leave_id):
    leave = get_object_or_404(LeaveRequest, id=leave_id)
    
    # Update the leave status to 'rejected'
    leave.status = 'rejected'
    leave.save()

    # Send notification to the student
    Notification.objects.create(
        user=leave.student,
        message=f"Your leave request for {leave.subject} has been rejected."
    )

    messages.error(request, "Leave request rejected successfully.")
    return redirect('dashboard')


def teacher_leave_request(request):
    """Teacher submits a leave request"""
    try:
        fm = Teacher.objects.get(custid=request.user)
    except Teacher.DoesNotExist:
        fm = None 

    if fm is not None:
        try:
            headings = teacherdashboardheading.objects.filter(school=fm.school).prefetch_related('teachersubmenu_set')
        except teacherdashboardheading.DoesNotExist:
            headings = None
    else:
        headings = None
    if request.method == "POST":
        if request.user.is_authenticated and request.user.role == 'teacher':  # Ensure only teachers can submit
            subject = request.POST.get("subject")
            from_date = request.POST.get("from_date")
            to_date = request.POST.get("to_date")
            purpose = request.POST.get("purpose")

            if not subject or not from_date or not to_date or not purpose:
                messages.error(request, "All fields are required.")
                return redirect('teacher_leave_request')

            # Save the leave request with the logged-in teacher
            leave_request = TeacherLeaveRequest.objects.create(
                teacher=request.user,  # Ensure user is assigned here
                subject=subject,
                from_date=from_date,
                to_date=to_date,
                purpose=purpose,
                status='pending'
            )

            # Notify admin
            admin_users = CustomUser.objects.filter(role__in=['accountant', 'admin'])
            for admin in admin_users:
                Notification.objects.create(
                    user=admin,
                    message=f"New teacher leave request from {request.user.username}"
                )

                

            messages.success(request, "Leave request submitted successfully!")
            return redirect('dashboard')

        else:
            messages.error(request, "You must be logged in as a teacher to submit a leave request.")
            return redirect('teacher_leave_request')

    return render(request, "teacher_leave_request.html",{'headings':headings,'fm':fm})



def admin_teacher_leave_requests(request):
    """Admin views all teacher leave requests"""
    try:
        a1 = SchoolDetails.objects.get(custid=request.user)
    except SchoolDetails.DoesNotExist:
        messages.error(request, "School details not found!")
        return redirect('admin_dashboard')
    leave_requests = TeacherLeaveRequest.objects.all().order_by('-created_at')

    context = {
        "leave_requests": leave_requests,'a1':a1
    }
    return render(request, "admin_teacher_leave_requests.html", context)


def admin_approve_teacher_leave(request, leave_id):
    """Admin approves teacher leave request"""
    leave_request = get_object_or_404(TeacherLeaveRequest, id=leave_id)
    leave_request.status = 'approved'
    leave_request.save()

    # Notify teacher
    Notification.objects.create(
        user=leave_request.teacher,
        message=f"Your leave request for {leave_request.subject} has been approved."
    )

    messages.success(request, "Leave approved successfully!")
    return redirect('admin_teacher_leave_requests')


def admin_reject_teacher_leave(request, leave_id):
    """Admin rejects teacher leave request"""
    leave_request = get_object_or_404(TeacherLeaveRequest, id=leave_id)
    leave_request.status = 'rejected'
    leave_request.save()

    # Notify teacher
    Notification.objects.create(
        user=leave_request.teacher,
        message=f"Your leave request for {leave_request.subject} has been rejected."
    )

    messages.success(request, "Leave rejected successfully!")
    return redirect('admin_teacher_leave_requests')


def admin_student_credentials(request):
    try:
        a1 = SchoolDetails.objects.get(custid=request.user)
    except SchoolDetails.DoesNotExist:
        messages.error(request, "School details not found!")
        return redirect('admin_dashboard')  
    asc=StudentCredentials.objects.filter(school=a1)
    return render(request,"admin_student_credentials.html",{'asc':asc,'a1':a1})

def admin_teacher_credentials(request):
    try:
        a1 = SchoolDetails.objects.get(custid=request.user)
    except SchoolDetails.DoesNotExist:
        messages.error(request, "School details not found!")
        return redirect('admin_dashboard')  # Redirect if school is not set up
    asc=TeacherCredentials.objects.filter(school=a1)
    return render(request,"admin_teacher_credentials.html",{'asc':asc,'a1':a1})


from django.contrib.auth.decorators import user_passes_test
from .models import Circular
from django.contrib import messages

def circular_list(request):
    try:
        a1 = SchoolDetails.objects.get(custid=request.user)
    except SchoolDetails.DoesNotExist:
        messages.error(request, "School details not found!")
        return redirect('admin_dashboard')
    circulars = Circular.objects.filter(school=a1).order_by('-created_at')
    return render(request, 'circular_list.html', {'circulars': circulars,'a1':a1})

def create_circular(request):
    try:
        a1 = SchoolDetails.objects.get(custid=request.user)
    except SchoolDetails.DoesNotExist:
        messages.error(request, "School details not found!")
        return redirect('admin_dashboard')
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        circular_image = request.FILES.get('circular_image')

        # Create the circular object
        circular = Circular.objects.create(
            title=title,
            content=content,
            sent_to_students='sent_to_students' in request.POST,
            sent_to_teachers='sent_to_teachers' in request.POST,
            circular_image = circular_image,
            school=a1
        )

        query = request.GET.get('q', '')  # Get search query
        circulars = Circular.objects.all().order_by('-created_at')  # Latest circulars first

        # Search filter
        if query:
            circulars = circulars.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            )

        # Pagination
        paginator = Paginator(circulars, 5)  # 5 circulars per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)


        messages.success(request, 'Circular created successfully!')
        return redirect('circular_list')

    return render(request, 'create_circular.html',{'a1':a1})

def edit_circular(request, pk):
    circular = get_object_or_404(Circular, pk=pk)

    if request.method == 'POST':
        circular.title = request.POST.get('title')
        circular.content = request.POST.get('content')

        # Handle image update
        if 'circular_image' in request.FILES:
            circular.circular_image = request.FILES['circular_image']

        circular.sent_to_students = 'sent_to_students' in request.POST
        circular.sent_to_teachers = 'sent_to_teachers' in request.POST

        circular.save()
        messages.success(request, 'Circular updated successfully!')
        return redirect('circular_list')

    return render(request, 'edit_circular.html', {'circular': circular})  


def delete_circular(request, pk):
    circular = get_object_or_404(Circular, pk=pk)

    if request.method == 'POST':
        circular.delete()
        messages.success(request, 'Circular deleted successfully!')
        return redirect('circular_list')

    return render(request, 'delete_circular.html', {'circular': circular})




def student_circular(request):
    try:
        i = studentadmission.objects.get(custid=request.user)
    except studentadmission.DoesNotExist:
        i = None
    circulars = Circular.objects.filter(sent_to_students=True).order_by('-created_at')
    return render(request, 'student_circular.html', {'circulars': circulars,'i':i})


def teacher_circular(request):
    try:
        fm = Teacher.objects.get(custid=request.user)
    except Teacher.DoesNotExist:
        fm = None 

    if fm is not None:
        try:
            headings = teacherdashboardheading.objects.filter(school=fm.school).prefetch_related('teachersubmenu_set')
        except teacherdashboardheading.DoesNotExist:
            headings = None
    else:
        headings = None
    circulars = Circular.objects.filter(sent_to_teachers=True).order_by('-created_at')
    return render(request, 'teacher_circular.html', {'circulars': circulars,'headings':headings,'fm':fm})


def student_fee_details(request):
    try:
        a1 = SchoolDetails.objects.get(custid=request.user)
    except SchoolDetails.DoesNotExist:
        messages.error(request, "School details not found!")
        return redirect('admin_dashboard')  
    classes = Class.objects.filter(school=a1).order_by('name').distinct()

    # Get filter values from the request
    selected_class = request.GET.get('class')
    selected_section = request.GET.get('section')
    student_name = request.GET.get('studentname')
    registration_no = request.GET.get('registrationno')

    fee_details = student_fee_Amount.objects.filter(school=a1)

    payment_details = StudentPayment.objects.all()

    if selected_class:
        fee_details = fee_details.filter(stdid__classs__id=selected_class, school=a1)

    if selected_section:
        fee_details = fee_details.filter(stdid__section__id=selected_section, school=a1)

    if student_name:
        fee_details = fee_details.filter(stdid__studentname__icontains=student_name, school=a1)

    if registration_no:
        fee_details = fee_details.filter(stdid__registrationno__icontains=registration_no, school=a1)
    

    
    for fee in fee_details:
        fee.paid_amount = fee.part1 + fee.part2 + fee.part3
        fee.balance = fee.total_amount - fee.paid_amount

    # Fetch sections dynamically based on the selected class
    sections = Section.objects.filter(class_assigned_id=selected_class, school=a1).distinct() if selected_class else Section.objects.none()

    context = {
        'classes': classes,
        'sections': sections,
        'selected_class': selected_class,
        'selected_section': selected_section,
        'student_name': student_name,
        'registration_no': registration_no,
        'fee_details': fee_details,
        'a1':a1
    }
    return render(request, "student_fee_details.html", context)

#=======================================SUBMENU==============================================================

# views.py
from django.shortcuts import render, redirect
from .models import teacherdashboardheading, teachersubmenu

def add_heading(request):
    try:
        a1 = SchoolDetails.objects.get(custid=request.user)
    except SchoolDetails.DoesNotExist:
        messages.error(request, "School details not found!")
        return redirect('admin_dashboard') 
    if request.method == 'POST':
        heading = request.POST.get('heading')
        if heading:
            teacherdashboardheading.objects.create(heading=heading,school=a1)
            return redirect('add_heading')
    return render(request, 'add_heading.html',{'a1':a1})


def add_submenu(request):
    try:
        a1 = SchoolDetails.objects.get(custid=request.user)
    except SchoolDetails.DoesNotExist:
        messages.error(request, "School details not found!")
        return redirect('admin_dashboard') 
    headings = teacherdashboardheading.objects.filter(school=a1)
    if request.method == 'POST':
        teacher_id = request.POST.get('teacherid')
        title = request.POST.get('title')
        url = request.POST.get('urls')
        if teacher_id and title and url:
            teachersubmenu.objects.create(
                teacherid_id=teacher_id,
                title=title,
                urls=url,
                school=a1,
            )
            return redirect('add_submenu')
    return render(request, 'add_submenu.html', {'headings': headings,'a1':a1})

from django.shortcuts import render, redirect
from .models import teacherdashboardheading, teachersubmenu

from django.shortcuts import render, redirect
from .models import teacherdashboardheading, teachersubmenu

def manage_teacher_dashboard(request):
    try:
        a1 = SchoolDetails.objects.get(custid=request.user)
    except SchoolDetails.DoesNotExist:
        messages.error(request, "School details not found!")
        return redirect('admin_dashboard') 
    heading_data = teacherdashboardheading.objects.filter(school=a1)
    submenu_data = teachersubmenu.objects.filter(school=a1)

    if request.method == 'POST':
        # HEADINGS SECTION
        if 'heading_submit' in request.POST:
            selected_ids = request.POST.getlist('heading_checkbox')
            for item in heading_data:
                item.status = 1 if str(item.id) in selected_ids else 0
                item.save()

        # SUBMENUS SECTION
        elif 'submenu_submit' in request.POST:
            selected_ids = request.POST.getlist('submenu_checkbox')
            for item in submenu_data:
                item.status = 1 if str(item.id) in selected_ids else 0
                item.save()

        return redirect('manage_teacher_dashboard')

    return render(request, 'dashboardsdata.html', {
        'heading_data': heading_data,
        'submenu_data': submenu_data,'a1':a1
    })

#########################################################################################
def get_user_school(user):
    return SchoolDetails.objects.filter(custid=user).first()

def gallery_list(request):
    try:
        a1 = SchoolDetails.objects.get(custid=request.user)
    except SchoolDetails.DoesNotExist:
        messages.error(request, "School details not found!")
        return redirect('admin_dashboard')
    school = get_user_school(request.user)
    albums = GalleryAlbum.objects.filter(school=school)
    return render(request, "gallery_list.html", {"albums": albums,'a1':a1})

def gallery_detail(request, album_id):
    school = get_user_school(request.user)
    album = get_object_or_404(GalleryAlbum, id=album_id, school=school)
    images = album.images.all()
    return render(request, "gallery_detail.html", {"album": album, "images": images})

def create_album(request):
    try:
        a1 = SchoolDetails.objects.get(custid=request.user)
    except SchoolDetails.DoesNotExist:
        messages.error(request, "School details not found!")
        return redirect('admin_dashboard')
    school = get_user_school(request.user)
    if request.method == "POST":
        title = request.POST.get("title")
        if title:
            album = GalleryAlbum.objects.create(title=title, created_by=request.user, school=school)
            return redirect("gallery_list")
    return render(request, "create_album.html",{'a1':a1})

def upload_image(request, album_id):
    school = get_user_school(request.user)
    album = get_object_or_404(GalleryAlbum, id=album_id, school=school)
    if request.method == "POST" and request.FILES.get("image"):
        image = request.FILES["image"]
        GalleryImage.objects.create(album=album, image=image, uploaded_by=request.user, school=school)
        return redirect("gallery_detail", album_id=album.id)
    return render(request, "upload_image.html", {"album": album})

def event_list(request):
    try:
        a1 = SchoolDetails.objects.get(custid=request.user)
    except SchoolDetails.DoesNotExist:
        messages.error(request, "School details not found!")
        return redirect('admin_dashboard')
    school = get_user_school(request.user)
    events = Event.objects.filter(school=school)
    return render(request, "event_list.html", {"events": events,'a1':a1})

def event_detail(request, event_id):
    school = get_user_school(request.user)
    event = get_object_or_404(Event, id=event_id, school=school)
    return render(request, "event_detail.html", {"event": event})

def create_event(request):
    try:
        a1 = SchoolDetails.objects.get(custid=request.user)
    except SchoolDetails.DoesNotExist:
        messages.error(request, "School details not found!")
        return redirect('admin_dashboard')
    school = get_user_school(request.user)
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        event_date = request.POST.get("event_date")
        venue = request.POST.get("venue")

        if title and event_date and venue:
            Event.objects.create(
                title=title,
                description=description,
                event_date=event_date,
                venue=venue,
                created_by=request.user,
                school=school
            )
            return redirect("event_list")
    return render(request, "create_event.html",{'a1':a1})

def student_gallery_list(request):
    
    school = get_user_school(request.user)
    albums = GalleryAlbum.objects.filter(school=school)
    return render(request, "student_gallery_list.html", {"albums": albums})

def student_gallery_detail(request, album_id):
    album = get_object_or_404(GalleryAlbum, id=album_id)
    images = album.images.all()
    return render(request, "student_gallery_detail.html", {"album": album, "images": images})

def student_event_list(request):
    school = get_user_school(request.user)
    events = Event.objects.filter(school=school)
    return render(request, "student_event_list.html", {"events": events})

def student_event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, "student_event_detail.html", {"event": event})

def teacher_gallery_list(request):
    try:
        fm = Teacher.objects.get(custid=request.user)
    except Teacher.DoesNotExist:
        fm = None 
    if fm is not None:
        try:
            headings = teacherdashboardheading.objects.filter(school=fm.school).prefetch_related('teachersubmenu_set')
        except teacherdashboardheading.DoesNotExist:
            headings = None
    else:
        headings = None
    albums = GalleryAlbum.objects.filter(school=fm.school)
    return render(request, "teacher_gallery_list.html", {"albums": albums,'headings':headings,'fm':fm})

def teacher_gallery_detail(request, album_id):
    try:
        fm = Teacher.objects.get(custid=request.user)
    except Teacher.DoesNotExist:
        fm = None 
    if fm is not None:
        try:
            headings = teacherdashboardheading.objects.filter(school=fm.school).prefetch_related('teachersubmenu_set')
        except teacherdashboardheading.DoesNotExist:
            headings = None
    else:
        headings = None
    album = get_object_or_404(GalleryAlbum, id=album_id)
    images = album.images.all()
    return render(request, "teacher_gallery_detail.html", {"album": album, "images": images,'headings':headings})

def teacher_create_album(request):
    try:
        fm = Teacher.objects.get(custid=request.user)
    except Teacher.DoesNotExist:
        fm = None 
    if fm is not None:
        try:
            headings = teacherdashboardheading.objects.filter(school=fm.school).prefetch_related('teachersubmenu_set')
        except teacherdashboardheading.DoesNotExist:
            headings = None
    else:
        headings = None
    if request.method == "POST":
        title = request.POST.get("title")
        if title:
            album = GalleryAlbum.objects.create(title=title, created_by=fm.custid, school=fm.school)
            return redirect("teacher_gallery_list")
    return render(request, "teacher_create_album.html",{'headings':headings,'fm':fm})

def teacher_upload_image(request, album_id):
    try:
        fm = Teacher.objects.get(custid=request.user)
    except Teacher.DoesNotExist:
        fm = None 
    if fm is not None:
        try:
            headings = teacherdashboardheading.objects.filter(school=fm.school).prefetch_related('teachersubmenu_set')
        except teacherdashboardheading.DoesNotExist:
            headings = None
    else:
        headings = None
    album = get_object_or_404(GalleryAlbum, id=album_id)
    if request.method == "POST" and request.FILES.get("image"):
        image = request.FILES["image"]
        GalleryImage.objects.create(album=album, image=image, uploaded_by=request.user)
        return redirect("teacher_gallery_detail", album_id=album.id)
    return render(request, "teacher_upload_image.html", {"album": album,'headings':headings})


#   try:
#         fm = Teacher.objects.get(custid=request.user)
#     except Teacher.DoesNotExist:
#         fm = None 

#     if fm is not None:
#         try:
#             headings = teacherdashboardheading.objects.filter(school=fm.school).prefetch_related('teachersubmenu_set')
#         except teacherdashboardheading.DoesNotExist:
#             headings = None
#     else:
#         headings = None

#     try:
#         assigned_class = AssignedClass.objects.get(custid=request.user)
#         assigned_class_name = assigned_class.class_assigned_id
#         sec = assigned_class.section_id

#         # Fetch students with matching class and section
#         students = studentadmission.objects.filter(
#             classs_id=assigned_class_name,
#             section_id=sec
#         )

#         print(f"DEBUG: Assigned Class - '{assigned_class_name}', Section - '{sec}'")
#         print(f"DEBUG: Found {students.count()} students")

#     except AssignedClass.DoesNotExist:
#         assigned_class = None
#         students = None
#         print("DEBUG: No AssignedClass found for this user.")

#     return render(request,"classteacherstd.html",{'students':students,'headings':headings})


def teacher_event_list(request):
    try:
        fm = Teacher.objects.get(custid=request.user)
    except Teacher.DoesNotExist:
        fm = None 
    if fm is not None:
        try:
            headings = teacherdashboardheading.objects.filter(school=fm.school).prefetch_related('teachersubmenu_set')
        except teacherdashboardheading.DoesNotExist:
            headings = None
    else:
        headings = None
        
    events = Event.objects.filter(school=fm.school)
    return render(request, "teacher_event_list.html", {"events": events,'headings':headings,'fm':fm})

def teacher_event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, "teacher_event_detail.html", {"event": event})

def teacher_create_event(request):
    try:
        fm = Teacher.objects.get(custid=request.user)
    except Teacher.DoesNotExist:
        fm = None 
    if fm is not None:
        try:
            headings = teacherdashboardheading.objects.filter(school=fm.school).prefetch_related('teachersubmenu_set')
        except teacherdashboardheading.DoesNotExist:
            headings = None
    else:
        headings = None
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        event_date = request.POST.get("event_date")
        venue = request.POST.get("venue")

        if title and event_date and venue:
            Event.objects.create(
                title=title,
                description=description,
                event_date=event_date,
                venue=venue,
                created_by=fm.custid,
                school=fm.school
            )
            return redirect("teacher_event_list")
    return render(request, "teacher_create_event.html",{'headings':headings,'fm':fm})

import zipfile

def download_images(request):
    if request.method == "POST":
        image_ids = request.POST.getlist('images')
        if not image_ids:
            return HttpResponse("No images selected", status=400)

        zip_filename = "selected_images.zip"
        response = HttpResponse(content_type="application/zip")
        response["Content-Disposition"] = f'attachment; filename="{zip_filename}"'

        with zipfile.ZipFile(response, "w") as zip_file:
            for image_id in image_ids:
                image = get_object_or_404(GalleryImage, id=image_id)
                image_path = image.image.path  
                zip_file.write(image_path, os.path.basename(image_path))  

        return response
    return HttpResponse("Invalid request", status=400)



def students_using_transport(request):
    try:
        a1 = SchoolDetails.objects.get(custid=request.user)
    except SchoolDetails.DoesNotExist:
        messages.error(request, "School details not found!")
        return redirect('admin_dashboard')
    school = get_user_school(request.user)
    students = TransportInformation.objects.filter(transport_available='yes', school=school)
    return render(request, 'students_using_transport.html', {'students': students,'a1':a1})

def students_not_using_transport(request):
    try:
        a1 = SchoolDetails.objects.get(custid=request.user)
    except SchoolDetails.DoesNotExist:
        messages.error(request, "School details not found!")
        return redirect('admin_dashboard')
    school = get_user_school(request.user)
    students = TransportInformation.objects.filter(transport_available='no', school=school)
    return render(request, 'students_not_using_transport.html', {'students': students,'a1':a1})

def non_teaching_staff_dashboard(request):
    staff = NonTeachingStaff.objects.get(user=request.user)
    school = staff.school

    today = now().date()
    transports = Transport.objects.filter(school=school)

    chart_data = []
    has_attendance_data = False  # flag to determine if we should show chart

    for transport in transports:
        total_present = TransportAttendance.objects.filter(
            transport=transport, status='Present', school=school, date=today
        ).count()
        total_absent = TransportAttendance.objects.filter(
            transport=transport, status='Absent', school=school, date=today
        ).count()

        if total_present > 0 or total_absent > 0:
            has_attendance_data = True

        chart_data.append({
            'bus_no': transport.vechile_number,
            'present': total_present,
            'absent': total_absent,
        })

    return render(request, 'non_teaching_staff_dashboard.html', {
        'chart_data': chart_data,
        'today': today,
        'has_attendance_data': has_attendance_data
    })


def add_non_teaching_staff(request):
    try:
        a1 = SchoolDetails.objects.get(custid=request.user)
    except SchoolDetails.DoesNotExist:
        messages.error(request, "School details not found!")
        return redirect('admin_dashboard')
    school = get_user_school(request.user)
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        designation = request.POST.get('designation')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        # Create user
        user = CustomUser.objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=make_password(password),
            role='non_teaching_staff',
        )

        # Create NonTeachingStaff profile
        NonTeachingStaff.objects.create(
            user=user,
            first_name = first_name,
            last_name = last_name,
            username = user.username,
            email = user.email,
            password = password,
            designation=designation,
            phone=phone,
            address=address,
            school=school
        )

        return redirect('non_teaching_staff_list')  # Or success page

    return render(request, 'add_non_teaching_staff.html',{'a1':a1})


def non_teaching_staff_list(request):
    try:
        a1 = SchoolDetails.objects.get(custid=request.user)
    except SchoolDetails.DoesNotExist:
        messages.error(request, "School details not found!")
        return redirect('admin_dashboard')
    school = get_user_school(request.user)
    staff_members = NonTeachingStaff.objects.filter(school=school)
    return render(request, "non_teaching_staff_list.html",{'staff_members':staff_members,'a1':a1})

def students_using_transport1(request):
    try:
        a1 = SchoolDetails.objects.get(custid=request.user)
    except SchoolDetails.DoesNotExist:
        messages.error(request, "School details not found!")
        return redirect('admin_dashboard')
    school = get_user_school(request.user)
    students = TransportInformation.objects.filter(transport_available='yes', school=school)
    return render(request, 'students_using_transport1.html', {'students': students,'a1':a1})

def students_not_using_transport1(request):
    try:
        a1 = SchoolDetails.objects.get(custid=request.user)
    except SchoolDetails.DoesNotExist:
        messages.error(request, "School details not found!")
        return redirect('admin_dashboard')
    school = get_user_school(request.user)
    students = TransportInformation.objects.filter(transport_available='no', school=school)
    return render(request, 'students_not_using_transport1.html', {'students': students,'a1':a1})


def add_transport(request):
    staff = NonTeachingStaff.objects.get(user=request.user)
    school = staff.school
    routes = Route.objects.filter(school=school)

    if request.method == "POST":
        vechile_name = request.POST.get('vechile_name')
        vechile_number = request.POST.get('vechile_number')
        date_of_purchase = request.POST.get('date_of_purchase')
        route_id = request.POST.get('route')  # get route ID from POST
        route = Route.objects.get(id=route_id) if route_id else None

        # Save the transport record
        Transport.objects.create(
            vechile_name=vechile_name,
            vechile_number=vechile_number,
            date_of_purchase=date_of_purchase,
            school=school,
            route=route
        )
        return redirect('transport_list')  # success redirect

    return render(request, 'add_transport.html', {'routes': routes})


def transport_list(request):
    
    staff = NonTeachingStaff.objects.get(user=request.user)
    school = staff.school
    transports = Transport.objects.filter(school=school)

    return render(request, 'transport_list.html', {'transports': transports})

def edit_transport(request, pk):
    staff = NonTeachingStaff.objects.get(user=request.user)
    school = staff.school
    routes = Route.objects.filter(school=school)


    transport = get_object_or_404(Transport, pk=pk, school=school)

    if request.method == 'POST':
        transport.vechile_name = request.POST.get('vechile_name')
        transport.vechile_number = request.POST.get('vechile_number')
        route_id = request.POST.get('route')  # get route ID from POST
        transport.route = Route.objects.get(id=route_id) if route_id else None
        transport.date_of_purchase = request.POST.get('date_of_purchase')
        transport.save()
        return redirect('transport_list')

    return render(request, 'edit_transport.html', {'transport': transport,'routes': routes,})

def delete_transport(request, pk):
    staff = NonTeachingStaff.objects.get(user=request.user)
    school = staff.school

    transport = get_object_or_404(Transport, pk=pk, school=school)
    transport.delete()
    return redirect('transport_list')


def drivers_list(request):
    
    staff = NonTeachingStaff.objects.get(user=request.user)
    school = staff.school
    drivers = Driver.objects.filter(school=school)

    return render(request, 'drivers_list.html', {'drivers': drivers})

def edit_driver(request, pk):
    staff = NonTeachingStaff.objects.get(user=request.user)
    school = staff.school

    driver = get_object_or_404(Driver, pk=pk, school=school)

    if request.method == "POST":
        driver.name = request.POST.get('name')
        driver.phone = request.POST.get('phone')
        driver.license_number = request.POST.get('license_number')
        driver.address = request.POST.get('address')
        driver.save()
        return redirect('drivers_list')

    return render(request, 'edit_driver.html', {'driver': driver})

def delete_driver(request, pk):
    staff = NonTeachingStaff.objects.get(user=request.user)
    school = staff.school

    driver = get_object_or_404(Driver, pk=pk, school=school)
    driver.delete()
    return redirect('drivers_list')



def add_driver(request):
    
    staff = NonTeachingStaff.objects.get(user=request.user)
    school = staff.school
    
    if request.method == "POST":
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        license_number = request.POST.get('license_number')
        address = request.POST.get('address')

        Driver.objects.create(
            name=name,
            phone=phone,
            license_number=license_number,
            address=address,
            school=school
        )

        messages.success(request, "Driver added successfully.")
        return redirect('assign_driver')  # or wherever you want to go next

    return render(request, "add_driver.html")


def assign_driver(request):
    try:
        staff = NonTeachingStaff.objects.get(user=request.user)
        school = staff.school
    except NonTeachingStaff.DoesNotExist:
        messages.error(request, "You are not registered as non-teaching staff.")
        return redirect('transport_list')

    transports = Transport.objects.filter(school=school)
    drivers = Driver.objects.filter(school=school)

    if request.method == "POST":
        transport_id = request.POST.get("transport_id")
        driver_id = request.POST.get("driver_id")

        transport = get_object_or_404(Transport, id=transport_id, school=school)
        driver = get_object_or_404(Driver, id=driver_id, school=school)

        transport.driver = driver
        transport.save()
        messages.success(request, "Driver assigned successfully.")
        return redirect('transport_list')

    return render(request, "assign_driver.html", {"transports": transports, "drivers": drivers})


def admin_transport_list(request):
    try:
        a1 = SchoolDetails.objects.get(custid=request.user)
    except SchoolDetails.DoesNotExist:
        messages.error(request, "School details not found!")
        return redirect('admin_dashboard')
    school = SchoolDetails.objects.get(custid=request.user)
    transports = Transport.objects.filter(school=school)
    return render(request, 'admin_transport_list.html', {'transports': transports,'a1':a1})

def admin_driver_list(request):
    try:
        a1 = SchoolDetails.objects.get(custid=request.user)
    except SchoolDetails.DoesNotExist:
        messages.error(request, "School details not found!")
        return redirect('admin_dashboard')
    school = SchoolDetails.objects.get(custid=request.user)
    drivers = Driver.objects.filter(school=school)
    return render(request, 'admin_driver_list.html', {'drivers': drivers,'a1':a1})


def add_route(request):
    try:
        a1 = SchoolDetails.objects.get(custid=request.user)
    except SchoolDetails.DoesNotExist:
        messages.error(request, "School details not found!")
        return redirect('admin_dashboard')
    staff = NonTeachingStaff.objects.get(user=request.user)
    school = staff.school

    if request.method == "POST":
        name = request.POST.get('name')
        start_point = request.POST.get('start_point')
        end_point = request.POST.get('end_point')
        stops = request.POST.get('stops')

        Route.objects.create(
            name=name,
            start_point=start_point,
            end_point=end_point,
            stops=stops,
            school=school
        )
        return redirect('add_route')  # Replace with your route list URL

    return render(request, 'add_route.html',{'a1':a1})

def route_list(request):
    try:
        a1 = SchoolDetails.objects.get(custid=request.user)
    except SchoolDetails.DoesNotExist:
        messages.error(request, "School details not found!")
        return redirect('admin_dashboard')
    staff = NonTeachingStaff.objects.get(user=request.user)
    school = staff.school
    routes = Route.objects.filter(school=school)

    return render(request, 'route_list.html', {'routes': routes,'a1':a1})    

def edit_route(request, pk):
    staff = NonTeachingStaff.objects.get(user=request.user)
    school = staff.school

    route = get_object_or_404(Route, pk=pk, school=school)  # filter by school

    if request.method == 'POST':
        route.name = request.POST.get('name')
        route.start_point = request.POST.get('start_point')
        route.end_point = request.POST.get('end_point')
        route.stops = request.POST.get('stops')
        route.save()
        return redirect('route_list')

    return render(request, 'edit_route.html', {'route': route})

def delete_route(request, pk):
    staff = NonTeachingStaff.objects.get(user=request.user)
    school = staff.school

    route = get_object_or_404(Route, pk=pk, school=school)  # filter by school

    route.delete()
    return redirect('route_list')


def transport_student_list(request):
    staff = NonTeachingStaff.objects.get(user=request.user)
    school = staff.school

    transports = Transport.objects.filter(school=school)

    selected_transport = request.GET.get('transport')


    students = TransportInformation.objects.filter(school=school)

    if selected_transport:
        students = students.filter(bus_no=selected_transport)


    total_students = students.count()

    context = {
        'transports': transports,
        'students': students,
        'selected_transport': selected_transport,
        'total_students': total_students
    }
    return render(request, 'transport_student_list.html', context)


from django.template.loader import render_to_string

def export_transport_pdf(request):
    staff = NonTeachingStaff.objects.get(user=request.user)
    school = staff.school

    transport = request.GET.get('transport')
    class_id = request.GET.get('class')
    section_id = request.GET.get('section')

    students = TransportInformation.objects.filter(school=school)
    if transport:
        students = students.filter(bus_no=transport)
    if class_id:
        students = students.filter(stdid__student_class_id=class_id)
    if section_id:
        students = students.filter(stdid__section_id=section_id)

    html = render_to_string('export_transport_pdf.html', {
        'students': students,
        'total_students': students.count()
    })

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="transport_students.pdf"'
    pisa.CreatePDF(BytesIO(html.encode("UTF-8")), dest=response)
    return response


def export_transport_excel(request):
    staff = NonTeachingStaff.objects.get(user=request.user)
    school = staff.school

    transport = request.GET.get('transport')
    class_id = request.GET.get('class')
    section_id = request.GET.get('section')

    students = TransportInformation.objects.filter(school=school)
    if transport:
        students = students.filter(bus_no=transport)
    if class_id:
        students = students.filter(stdid__student_class_id=class_id)
    if section_id:
        students = students.filter(stdid__section_id=section_id)

    data = []
    for s in students:
        data.append({
            'Admission No': s.stdid.registrationno,
            'Name': s.stdid.studentname,
            'Class': s.stdid.classs,
            'Section': s.stdid.section.name,
            'Bus No': s.bus_no,
            'Driver': s.driver_name,
            'Route': s.route,
        })

    df = pd.DataFrame(data)
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Students')

    buffer.seek(0)
    response = HttpResponse(
        buffer,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="transport_students.xlsx"'
    return response

def admin_transport_student_list(request):
    try:
        a1 = SchoolDetails.objects.get(custid=request.user)
    except SchoolDetails.DoesNotExist:
        messages.error(request, "School details not found!")
        return redirect('admin_dashboard')
    school = SchoolDetails.objects.get(custid=request.user)

    transports = Transport.objects.filter(school=school)

    selected_transport = request.GET.get('transport')


    students = TransportInformation.objects.filter(school=school)

    if selected_transport:
        students = students.filter(bus_no=selected_transport)


    total_students = students.count()

    context = {
        'transports': transports,
        'students': students,
        'selected_transport': selected_transport,
        'total_students': total_students,
        'a1':a1
    }
    return render(request, 'admin_transport_student_list.html', context)

def admin_export_transport_pdf(request):
    school = SchoolDetails.objects.get(custid=request.user)

    transport = request.GET.get('transport')
    class_id = request.GET.get('class')
    section_id = request.GET.get('section')

    students = TransportInformation.objects.filter(school=school)
    if transport:
        students = students.filter(bus_no=transport)
    if class_id:
        students = students.filter(stdid__student_class_id=class_id)
    if section_id:
        students = students.filter(stdid__section_id=section_id)

    html = render_to_string('export_transport_pdf.html', {
        'students': students,
        'total_students': students.count()
    })

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="transport_students.pdf"'
    pisa.CreatePDF(BytesIO(html.encode("UTF-8")), dest=response)
    return response


def admin_export_transport_excel(request):
    school = SchoolDetails.objects.get(custid=request.user)

    transport = request.GET.get('transport')
    class_id = request.GET.get('class')
    section_id = request.GET.get('section')

    students = TransportInformation.objects.filter(school=school)
    if transport:
        students = students.filter(bus_no=transport)
    if class_id:
        students = students.filter(stdid__student_class_id=class_id)
    if section_id:
        students = students.filter(stdid__section_id=section_id)

    data = []
    for s in students:
        data.append({
            'Admission No': s.stdid.registrationno,
            'Name': s.stdid.studentname,
            'Class': s.stdid.classs,
            'Section': s.stdid.section.name,
            'Bus No': s.bus_no,
            'Driver': s.driver_name,
            'Route': s.route,
        })

    df = pd.DataFrame(data)
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Students')

    buffer.seek(0)
    response = HttpResponse(
        buffer,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="transport_students.xlsx"'
    return response

def mark_transport_attendance(request):
    staff = NonTeachingStaff.objects.get(user=request.user)
    school = staff.school
    transports = Transport.objects.filter(school=school)
    selected_transport = request.GET.get('transport')
    selected_date = request.GET.get('date', timezone.now().date())

    students = TransportInformation.objects.filter(school=school, bus_no=selected_transport) if selected_transport else []

    if request.method == 'POST':
        for student_info in students:
            status = request.POST.get(f'attendance_{student_info.stdid.id}')
            TransportAttendance.objects.update_or_create(
                student=student_info.stdid,
                transport=Transport.objects.get(vechile_number=selected_transport),
                date=selected_date,
                school=school,
                defaults={'status': status}
            )
        messages.success(request, "Attendance saved successfully.")
        return redirect('mark_transport_attendance')

    context = {
        'transports': transports,
        'students': students,
        'selected_transport': selected_transport,
        'selected_date': selected_date,
    }
    return render(request, 'mark_transport_attendance.html', context)

from django.utils import timezone

def view_transport_attendance(request):
    staff = NonTeachingStaff.objects.get(user=request.user)
    school = staff.school
    transports = Transport.objects.filter(school=school)

    selected_transport = request.GET.get('transport')
    selected_date = request.GET.get('date', timezone.now().date())

    attendance_records = []
    total_present = total_absent = 0

    if selected_transport and selected_date:
        attendance_records = TransportAttendance.objects.filter(
            school=school,
            transport__vechile_number=selected_transport,
            date=selected_date
        )

        total_present = attendance_records.filter(status='Present').count()
        total_absent = attendance_records.filter(status='Absent').count()


    context = {
        'transports': transports,
        'selected_transport': selected_transport,
        'selected_date': selected_date,
        'attendance_records': attendance_records,
        'total_present': total_present,
        'total_absent': total_absent,
    }
    return render(request, 'view_transport_attendance.html', context)

def admin_view_transport_attendance(request):
    try:
        a1 = SchoolDetails.objects.get(custid=request.user)
    except SchoolDetails.DoesNotExist:
        messages.error(request, "School details not found!")
        return redirect('admin_dashboard')
    school = SchoolDetails.objects.get(custid=request.user)
    transports = Transport.objects.filter(school=school)

    selected_transport = request.GET.get('transport')
    selected_date = request.GET.get('date', timezone.now().date())

    attendance_records = []
    total_present = total_absent = 0

    if selected_transport and selected_date:
        attendance_records = TransportAttendance.objects.filter(
            school=school,
            transport__vechile_number=selected_transport,
            date=selected_date
        )

        total_present = attendance_records.filter(status='Present').count()
        total_absent = attendance_records.filter(status='Absent').count()


    context = {
        'transports': transports,
        'selected_transport': selected_transport,
        'selected_date': selected_date,
        'attendance_records': attendance_records,
        'total_present': total_present,
        'total_absent': total_absent,
        'a1':a1
    }
    return render(request, 'admin_view_transport_attendance.html', context)



def transport_attendance_summary(request):
    try:
        a1 = SchoolDetails.objects.get(custid=request.user)
    except SchoolDetails.DoesNotExist:
        messages.error(request, "School details not found!")
        return redirect('admin_dashboard')
    staff = NonTeachingStaff.objects.get(user=request.user)
    school = staff.school

    transports = Transport.objects.filter(school=school)
    selected_date = request.GET.get('date')

    summary_data = []
    chart_labels = []
    chart_present = []
    chart_absent = []

    if selected_date:
        for transport in transports:
            attendance_records = TransportAttendance.objects.filter(
                transport=transport,
                date=selected_date,
                school=school
            )
            present_count = attendance_records.filter(status='Present').count()
            absent_count = attendance_records.filter(status='Absent').count()

            summary_data.append({
                'transport': transport,
                'present': present_count,
                'absent': absent_count
            })

            chart_labels.append(transport.vechile_number)
            chart_present.append(present_count)
            chart_absent.append(absent_count)

    context = {
        'transports': transports,
        'selected_date': selected_date,
        'summary_data': summary_data,
        'chart_labels': chart_labels,
        'chart_present': chart_present,
        'chart_absent': chart_absent,
        'a1':a1
    }
    return render(request, 'transport_attendance_summary.html', context)

def admin_transport_attendance_summary(request):
    try:
        a1 = SchoolDetails.objects.get(custid=request.user)
    except SchoolDetails.DoesNotExist:
        messages.error(request, "School details not found!")
        return redirect('admin_dashboard')
    school = SchoolDetails.objects.get(custid=request.user)

    transports = Transport.objects.filter(school=school)
    selected_date = request.GET.get('date')

    summary_data = []
    chart_labels = []
    chart_present = []
    chart_absent = []


    if selected_date:
        for transport in transports:
            attendance_records = TransportAttendance.objects.filter(
                transport=transport,
                date=selected_date,
                school=school
            )
            present_count = attendance_records.filter(status='Present').count()
            absent_count = attendance_records.filter(status='Absent').count()

            summary_data.append({
                'transport': transport,
                'present': present_count,
                'absent': absent_count
            })
            chart_labels.append(transport.vechile_number)
            chart_present.append(present_count)
            chart_absent.append(absent_count)

    context = {
        'transports': transports,
        'selected_date': selected_date,
        'summary_data': summary_data,
        'chart_labels': chart_labels,
        'chart_present': chart_present,
        'chart_absent': chart_absent,
        'a1':a1
    }
    return render(request, 'admin_transport_attendance_summary.html', context)    


def student_attendance_history(request):
  
    try:
        i = studentadmission.objects.get(custid=request.user)
    except studentadmission.DoesNotExist:
        i = None  
    user = request.user
    student = studentadmission.objects.get(custid=user)
    school = student.school

    try:
        transport_info = TransportInformation.objects.get(stdid=student, school=school)
        transport = Transport.objects.get(vechile_number=transport_info.bus_no, school=school)
        driver = transport.driver
    except (TransportInformation.DoesNotExist, Transport.DoesNotExist):
        transport_info = None
        transport = None
        driver = None

    attendance_records = TransportAttendance.objects.filter(
        student=student,
        school=school
    ).order_by('-date')

    total_present = attendance_records.filter(status="Present").count()
    total_absent = attendance_records.filter(status="Absent").count()

    return render(request, 'student_attendance_history.html', {
        'attendance_records': attendance_records,
        'transport_info': transport_info,
        'transport': transport,
        'driver': driver,
        'total_present': total_present,
        'total_absent': total_absent,
        'i':i
        
    })



from datetime import date
from .models import studentadmission, TransportAttendance, TransportInformation, Transport

def student_transport_details1(request):
    try:
        i = studentadmission.objects.get(custid=request.user)
    except studentadmission.DoesNotExist:
        i = None
    student = studentadmission.objects.get(custid=request.user)
    school = student.school

    today = date.today()
    absent_today = False

    try:
        attendance = TransportAttendance.objects.get(student=student, date=today, school=school)
        if attendance.status == 'Absent':
            absent_today = True
    except TransportAttendance.DoesNotExist:
        absent_today = True

    transport_info = TransportInformation.objects.filter(stdid=student, school=school).first()

    transport = None
    driver = None
    if transport_info:
        if isinstance(transport_info.bus_no, Transport):
            transport = transport_info.bus_no
        else:
            transport = Transport.objects.filter(vechile_number=transport_info.bus_no, school=school).first()

        if transport:
            driver = transport.driver

    return render(request, 'student_transport_details1.html', {
        'transport_info': transport_info,
        'transport': transport,
        'driver': driver,
        'absent_today': absent_today,
        'i':i
    })

def report_transport_issue(request):
    student = studentadmission.objects.get(custid=request.user)
    school = student.school

    if request.method == 'POST':
        issue_type = request.POST.get('issue_type')
        description = request.POST.get('description')

        TransportIssue.objects.create(
            student=student,
            school=school,
            issue_type=issue_type,
            description=description
        )
        messages.success(request, "Issue reported successfully.")
        return redirect('report_transport_issue')

    return render(request, 'report_transport_issue.html')

def transport_issues(request):
    staff = NonTeachingStaff.objects.get(user=request.user)
    school = staff.school
    issues = TransportIssue.objects.filter(school=school).order_by('-date_reported')

    return render(request, 'transport_issues.html', {
        'issues': issues
    })

def resolve_transport_issue(request, issue_id):
    issue = get_object_or_404(TransportIssue, id=issue_id)
    issue.status = 'Resolved'
    issue.save()
    messages.success(request, "Issue marked as resolved.")
    return redirect('transport_issues')

def admin_transport_issues(request):
    try:
        a1 = SchoolDetails.objects.get(custid=request.user)
    except SchoolDetails.DoesNotExist:
        messages.error(request, "School details not found!")
        return redirect('admin_dashboard')
    school = SchoolDetails.objects.get(custid=request.user)
    issues = TransportIssue.objects.filter(school=school).order_by('-date_reported')

    return render(request, 'admin_transport_issues.html', {
        'issues': issues,'a1':a1
    })

def admin_resolve_transport_issue(request, issue_id):
    issue = get_object_or_404(TransportIssue, id=issue_id)
    issue.status = 'Resolved'
    issue.save()
    messages.success(request, "Issue marked as resolved.")
    return redirect('admin_transport_issues')    




def select_user_to_chat(request):
    try:
        i = studentadmission.objects.get(custid=request.user)
    except studentadmission.DoesNotExist:
        i = None
    student = studentadmission.objects.get(custid=request.user)
    school = student.school

    # Admins (1 admin per school)
    admins = CustomUser.objects.filter(
        role='admin',
        id=school.custid.id
    )

    # Teachers
    teacher_qs = Teacher.objects.filter(
        school=school,
        custid__role='teacher'
    ).select_related('custid')

    # Build a list of teacher CustomUsers with display_name
    teacher_users = []
    for teacher in teacher_qs:
        user = teacher.custid
        user.display_name = teacher.first_name or user.username
        teacher_users.append(user)

    # Add display_name for admin
    admin_users = []
    for admin in admins:
        admin.display_name = admin.first_name or "Admin"
        admin_users.append(admin)


    # Combine
    users = admin_users + teacher_users
    users = [u for u in users if u.id != request.user.id]  # exclude self

    # Attach unread message count for each user
    for user in users:
        unread_count = Message.objects.filter(
            sender=user,
            recipient=request.user,
            is_read=False
        ).count()
        user.unread_count = unread_count
    

    return render(request, 'select_user.html', {'users': users,'i':i})


from django.utils.timezone import localtime

def chat_with_user(request, user_id):
    try:
        i = studentadmission.objects.get(custid=request.user)
    except studentadmission.DoesNotExist:
        i = None
    recipient = get_object_or_404(CustomUser, id=user_id)


    extra_name = ''
    if recipient.role == 'student':
        try:
            student = studentadmission.objects.get(custid=recipient)
            extra_name = student.studentname
        except studentadmission.DoesNotExist:
            extra_name = recipient.first_name  # fallback
    elif recipient.role == 'teacher':
        extra_name = f"{recipient.first_name} {recipient.last_name}"
    elif recipient.role == 'admin':
        extra_name = f"Admin"   
    else:
        extra_name = recipient.first_name  # fallback



    # Mark messages as read (that were sent to the current user by the recipient)
    Message.objects.filter(
        sender=recipient,
        recipient=request.user,
        is_read=False
    ).update(is_read=True)
    
    if request.method == 'POST':
        content = request.POST.get('content')
        attachment = request.FILES.get('attachment')
        if content or attachment:
            Message.objects.create(
                sender=request.user,
                recipient=recipient,  
                content=content,
                attachment=attachment
            )

    messages_qs = Message.objects.filter(
        sender__in=[request.user, recipient],
        recipient__in=[request.user, recipient] 
    ).order_by('timestamp')

    # Optional: convert timestamps to localtime (if needed manually)
    for msg in messages_qs:
        msg.timestamp = localtime(msg.timestamp)

    # Determine base template dynamically
    if request.user.role == 'student':
        base_template = 'student_base.html'
    elif request.user.role == 'teacher':
        base_template = 'teacher_base.html'
    else:
        base_template = 'admin_base.html'  # fallback

    # If it's an AJAX request, return rendered message list
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('messages_list.html', {
            'messages': messages_qs,
            'user': request.user
        })
        return JsonResponse({'html': html})    

    return render(request, 'chat.html', {
        'recipient': recipient,
        'messages': messages_qs,
        'base_template': base_template,
        'display_name': extra_name,
        'i':i
    })

from .models import studentadmission

def inbox(request):
    try:
        a1 = SchoolDetails.objects.get(custid=request.user)
    except SchoolDetails.DoesNotExist:
        messages.error(request, "School details not found!")
        return redirect('admin_dashboard')
    received_msgs = Message.objects.filter(recipient=request.user).order_by('-timestamp')
    senders = {}
    for msg in received_msgs:
        if msg.sender.id not in senders:
            senders[msg.sender.id] = msg

    # Attach student details to each message (if sender is student)
    enriched_messages = []
    for msg in senders.values():
        student_info = None
        if msg.sender.role == 'student':
            student_info = studentadmission.objects.filter(custid=msg.sender).select_related('classs', 'section').first()
        enriched_messages.append({
            'message': msg,
            'student': student_info
        })

    return render(request, 'inbox.html', {'messages': enriched_messages,'a1':a1})


def set_typing_status(request):
    if request.method == 'POST':
        sender = request.user
        recipient_id = request.POST.get('recipient_id')
        is_typing = request.POST.get('is_typing') == 'true'

        if recipient_id:
            recipient = CustomUser.objects.get(id=recipient_id)
            TypingStatus.objects.update_or_create(
                user=sender, recipient=recipient,
                defaults={'is_typing': is_typing}
            )
            return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'}, status=400)

def get_typing_status(request, user_id):
    other_user = CustomUser.objects.get(id=user_id)
    typing_status = TypingStatus.objects.filter(user=other_user, recipient=request.user, is_typing=True).first()

    return JsonResponse({
        'is_typing': typing_status is not None
    })

def upload_class_photo(request):
    try:
        fm = Teacher.objects.get(custid=request.user)
    except Teacher.DoesNotExist:
        fm = None 

    if fm is not None:
        try:
            headings = teacherdashboardheading.objects.filter(school=fm.school).prefetch_related('teachersubmenu_set')
        except teacherdashboardheading.DoesNotExist:
            headings = None
    else:
        headings = None

    # Get the classes and exams for that school
    classes = Class.objects.filter(school=fm.school).order_by('name').distinct()
    examms = exam.objects.filter(school=fm.school)

    if request.method == 'POST' and request.FILES.get('photo'):
        class_id = request.POST.get('class_name')
        section_id = request.POST.get('section')
        exam_id = request.POST.get('examm')
        photo = request.FILES['photo']

        # Fetch the actual model instances
        class_instance = Class.objects.get(id=class_id)
        section_instance = Section.objects.get(id=section_id)
        exam_instance = exam.objects.get(id=exam_id)

        # Create and save the ClassPhoto object
        class_photo = ClassPhoto1(
            school=fm.school,
            class_name=class_instance,
            section=section_instance,
            exam=exam_instance,
            photo=photo
        )
        class_photo.save()

        return redirect('upload_class_photo')  # Replace with your actual success URL

    return render(request, 'upload_class_photo.html', {
        'classes': classes,
        'examms': examms,
        'headings': headings,
        'fm':fm
    })


def get_sections3(request):
    """
    AJAX request to get sections by class ID.
    """
    class_id = request.GET.get('class_id')

    if class_id:
        sections = Section.objects.filter(class_assigned_id=class_id).values('id', 'name')
    else:
        sections = []

    return JsonResponse({'sections': list(sections)})




from django.template.loader import render_to_string


def admin_generate_reportcard(request):
    try:
        a1 = SchoolDetails.objects.get(custid=request.user)
    except SchoolDetails.DoesNotExist:
        messages.error(request, "School details not found!")
        return redirect('admin_dashboard')
    user = request.user
    school = SchoolDetails.objects.get(custid=user)

    # Fetch classes and exams
    classes = Class.objects.filter(school=school)
    exams = exam.objects.filter(school=school)
    sections = Section.objects.none()  # Default empty sections

    # Initialize variables
    students = []
    results = []
    selected_class = selected_section = selected_exam = None

    # Initialize exam_id outside POST block
    exam_id = None

    if request.method == 'POST':
        class_id = request.POST.get('class_name')
        section_id = request.POST.get('section')
        exam_id = request.POST.get('exam_id')

        selected_class = class_id
        selected_section = section_id
        selected_exam = exam_id

        if class_id and section_id and exam_id:
            # Fetch students based on the selected filters
            students = studentadmission.objects.filter(classs_id=class_id, section_id=section_id, school=school)
            results = StudentMarks1.objects.filter(student__in=students, exam_id=exam_id)
            sections = Section.objects.filter(class_assigned_id=class_id)  # To repopulate on POST

    # Fetch the exam object for the selected exam_id
    exam_obj = get_object_or_404(exam, id=exam_id) if exam_id else None

    report_data = []
    
    # Loop through each student to gather their report card data
    for student in students:
        total_obtained = 0
        total_max_marks = 0

        # Fetch all marks for the student in the selected exam
        marks = StudentMarks1.objects.filter(student=student, exam=exam_obj).select_related('subject')

        # Fetch extra subject marks
        extra_subjects = ExtraSubjectMarks.objects.filter(student=student, exam=exam_obj)

        # Fetch individual marks from SubjectMarksDetail
        marks_details = SubjectMarksDetail.objects.filter(student=student, exam=exam_obj).select_related('subject')

        # Retrieve Co-Scholastic grading scale
        co_scholastic_grades = CoScholasticGrade.objects.all()

        # Retrieve discipline grade for the student and exam
        discipline_grade = DisciplineGrade.objects.filter(student=student, exam=exam_obj).first()

        # Retrieve remarks
        remark = Remark.objects.filter(student=student, exam=exam_obj).first()

        # Retrieve signature and report date
        signature = ReportCardSignature.objects.filter(student=student, exam=exam_obj).first()

        # Organize marks into individual categories
        student_report_data = []
        for index, mark in enumerate(marks_details, start=1):
            total = mark.total
            total_obtained += total
            total_max_marks += 100

            # Grade Calculation
            if total >= 91:
                grade = "A1"
            elif total >= 81:
                grade = "A2"
            elif total >= 71:
                grade = "B1"
            elif total >= 61:
                grade = "B2"
            elif total >= 51:
                grade = "C1"
            elif total >= 41:
                grade = "C2"
            else:
                grade = "D"

            student_report_data.append({
                'sno': index,
                'subject': mark.subject.name,
                'pa': mark.pa,
                'se': mark.se,
                'ma': mark.ma,
                'nb': mark.nb,
                'term': mark.term,
                'total': mark.total,
                'grade': grade,
            })

        # Calculate overall percentage
        percentage = round((total_obtained / total_max_marks) * 100, 2) if total_max_marks > 0 else 0

        # Filter photo based on user school, class, section, and exam
        class_photo = ClassPhoto1.objects.filter(
            school=school,
            class_name=student.classs,
            section=student.section,
            exam=exam_obj
        ).first()

        # Append each student's report data to the overall report
        report_data.append({
            'student': student,
            'report_data': student_report_data,
            'total_obtained': total_obtained,
            'total_max_marks': total_max_marks,
            'percentage': percentage,
            'extra_subjects': extra_subjects,
            'co_scholastic_grades': co_scholastic_grades,
            'discipline_grade': discipline_grade,
            'remark': remark,
            'signature': signature,
            'class_photo': class_photo,
        })

    return render(request, "admin_generate_reportcard.html", {
        'classes': classes,
        'exams': exams,
        'sections': sections,
        'students': students,
        'results': results,
        'selected_class': selected_class,
        'selected_section': selected_section,
        'selected_exam': selected_exam,
        'report_data': report_data,  # Pass the report data for each student
        'a1':a1
    })


def get_sections4(request):
    """
    AJAX request to get sections by class ID.
    """
    class_id = request.GET.get('class_id')

    if class_id:
        sections = Section.objects.filter(class_assigned_id=class_id).values('id', 'name')
    else:
        sections = []

    return JsonResponse({'sections': list(sections)})



from django.shortcuts import render, get_object_or_404

def student_report_card(request):
    # Get the current logged-in student
    try:
        i = studentadmission.objects.get(custid=request.user)
    except studentadmission.DoesNotExist:
        i = None
    student = studentadmission.objects.get(custid=request.user)

    # Get the student's school
    school = student.school

    # Filter exams based on the student's school
    exams = exam.objects.filter(school=school)

    if request.method == 'POST':
        selected_exam_id = request.POST.get('exam')  # Fetch the selected exam ID from the form
        selected_exam = get_object_or_404(exam, id=selected_exam_id)  # Get the exam object

        # Fetch all subjects and marks for the student in the selected exam
        marks = StudentMarks1.objects.filter(
            student=student, 
            exam=selected_exam
        ).select_related('subject')

        # Fetch extra subject marks (if any)
        extra_subjects = ExtraSubjectMarks.objects.filter(
            student=student, 
            exam=selected_exam
        )

        # Fetch individual marks from SubjectMarksDetail
        marks_details = SubjectMarksDetail.objects.filter(
            student=student,
            exam=selected_exam
        ).select_related('subject')

        # Retrieve Co-Scholastic grading scale
        co_scholastic_grades = CoScholasticGrade.objects.all()

        # Retrieve discipline grade for the student and exam
        discipline_grade = DisciplineGrade.objects.filter(student=student, exam=selected_exam).first()

        # Retrieve remarks
        remark = Remark.objects.filter(student=student, exam=selected_exam).first()

        # Retrieve signature and report date
        signature = ReportCardSignature.objects.filter(student=student, exam=selected_exam).first()

        # Organize marks into individual categories
        report_data = []
        total_obtained = 0
        total_max_marks = 0

        for index, mark in enumerate(marks_details, start=1):
            total = mark.total
            total_obtained += total
            total_max_marks += 100

            # Grade Calculation
            if total >= 91:
                grade = "A1"
            elif total >= 81:
                grade = "A2"
            elif total >= 71:
                grade = "B1"
            elif total >= 61:
                grade = "B2"
            elif total >= 51:
                grade = "C1"
            elif total >= 41:
                grade = "C2"
            else:
                grade = "D"

            report_data.append({
                'sno': index,
                'subject': mark.subject.name,
                'pa': mark.pa,
                'se': mark.se,
                'ma': mark.ma,
                'nb': mark.nb,
                'term': mark.term,
                'total': mark.total,
                'grade': grade,
            })

        # Calculate overall percentage
        percentage = round((total_obtained / total_max_marks) * 100, 2) if total_max_marks > 0 else 0


        # Filter class photo for the selected exam and student
        class_photo = ClassPhoto1.objects.filter(
            school=school,
            class_name=student.classs,
            section=student.section,
            exam=selected_exam
        ).first()

        # Prepare the context for rendering
        context = {
            'student': student,
            'exam': selected_exam,
            'report_data': report_data,
            'total_obtained': total_obtained,
            'total_max_marks': total_max_marks,
            'percentage': percentage,
            'extra_subjects': extra_subjects,
            'co_scholastic_grades': co_scholastic_grades,
            'discipline_grade': discipline_grade,
            'remark': remark,
            'signature': signature,
            'class_photo': class_photo,
            'exams': exams,  # Make sure the list of exams is passed to the template
            'i':i
        }

        return render(request, 'student_exam_report_card.html', context)

    return render(request, 'student_report_card.html', {'exams': exams,'i':i})

def mark_notifications_read(request):
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return JsonResponse({'status': 'success'})



def lead_sources(request):
    a1 = SchoolDetails.objects.get(custid=request.user)
    if request.method == 'POST':
        name = request.POST.get('source_name')
        if name:
            LeadSource.objects.create(name=name,school=a1)
            messages.success(request, "Lead source added successfully!")
            return redirect('lead_sources')
    
    sources = LeadSource.objects.filter(school=a1).order_by('-created_at')
    return render(request, 'lead_sources.html', {'sources': sources,'a1':a1})

def edit_source(request, pk):
    source = get_object_or_404(LeadSource, pk=pk)
    if request.method == 'POST':
        name = request.POST.get('source_name')
        if name:
            source.name = name
            source.save()
            messages.success(request, "Lead source updated!")
            return redirect('lead_sources')
    return render(request, 'edit_source.html', {'source': source})

def delete_source(request, pk):
    source = get_object_or_404(LeadSource, pk=pk)
    source.delete()
    messages.success(request, "Lead source deleted!")
    return redirect('lead_sources')


def lead_statuses(request):
    a1 = SchoolDetails.objects.get(custid=request.user)
    if request.method == 'POST':
        name = request.POST.get('status_name')
        text_color = request.POST.get('text_color') or '#000000'
        bg_color = request.POST.get('bg_color') or '#FFFFFF'
        if name:
            LeadStatus.objects.create(name=name, text_color=text_color, bg_color=bg_color,school=a1)
            messages.success(request, "Lead status added successfully!")
            return redirect('lead_statuses')
    
    statuses = LeadStatus.objects.filter(school=a1).order_by('-created_at')
    return render(request, 'lead_statuses.html', {'statuses': statuses,'a1':a1})

def edit_status(request, pk):
    status = get_object_or_404(LeadStatus, pk=pk)
    if request.method == 'POST':
        status.name = request.POST.get('status_name')
        status.text_color = request.POST.get('text_color')
        status.bg_color = request.POST.get('bg_color')
        status.save()
        messages.success(request, "Lead status updated!")
        return redirect('lead_statuses')
    return render(request, 'edit_status.html', {'status': status})

def delete_status(request, pk):
    status = get_object_or_404(LeadStatus, pk=pk)
    status.delete()
    messages.success(request, "Lead status deleted!")
    return redirect('lead_statuses')


def leads_list(request):
    a1 = SchoolDetails.objects.get(custid=request.user)
    classes1 = Class.objects.filter(school=a1).order_by('name').distinct()
    sources = LeadSource.objects.filter(school=a1)
    leads = Lead.objects.filter(school=a1).order_by('-id')
    statuses = LeadStatus.objects.filter(school=a1).order_by('-id')
    employees = Teacher.objects.filter(school=a1).order_by('-id')

    if request.method == "POST":
        if 'update_status' in request.POST:
            lead = get_object_or_404(Lead, id=request.POST.get('lead_id'), school=a1)
            lead.status_id = request.POST.get('status')
            lead.scheduled_at = request.POST.get('scheduled_at') or None
            lead.remark = request.POST.get('remark')
            lead.save()
            return redirect('leads_list')

        if 'assign_lead' in request.POST:
            lead = get_object_or_404(Lead, id=request.POST.get('assign_lead_id'), school=a1)
            lead.assigned_to_id = request.POST.get('assigned_to')
            lead.status_id = request.POST.get('status')
            lead.scheduled_at = request.POST.get('scheduled_at') or None
            lead.remark = request.POST.get('remark')
            lead.save()
            return redirect('leads_list')

    return render(request, 'leads_list.html', {
        'leads': leads,
        'statuses': statuses,
        'classes1': classes1,
        'sources': sources,
        'a1': a1,
        'employees': employees
    })

def view_lead(request, id):
    obj = Lead.objects.get(id=id)
    return render(request,"view_lead.html",{'obj':obj})    


def add_lead(request):

    a1 = SchoolDetails.objects.get(custid=request.user)
    classes1 = Class.objects.filter(school=a1).order_by('name').distinct()
    sources = LeadSource.objects.filter(school=a1)
     

    if request.method == 'POST':
        admission_class = request.POST.get('admission_class')
        source_id = request.POST.get('source')
        source_obj = LeadSource.objects.get(id=source_id,school=a1)


        referred_by = request.POST.get('referred_by')

        # Student Details
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')

        # Parents Details - Mother
        mother_name = request.POST.get('mother_name')
        mother_qualification = request.POST.get('mother_qualification')
        mother_res_address = request.POST.get('mother_res_address')
        mother_occupation = request.POST.get('mother_occupation')
        mother_official_address = request.POST.get('mother_official_address')
        mother_income = request.POST.get('mother_income')
        mother_email = request.POST.get('mother_email')
        mother_mobile = request.POST.get('mother_mobile')

        # Parents Details - Father
        father_name = request.POST.get('father_name')
        father_qualification = request.POST.get('father_qualification')
        father_res_address = request.POST.get('father_res_address')
        father_occupation = request.POST.get('father_occupation')
        father_official_address = request.POST.get('father_official_address')
        father_income = request.POST.get('father_income')
        father_email = request.POST.get('father_email')
        father_mobile = request.POST.get('father_mobile')

        # Religion & Category
        nationality = request.POST.get('nationality')
        religion = request.POST.get('religion')
        category = request.POST.get('category')
        aadhar_no = request.POST.get('aadhar_no')

        # Last School Info
        last_school_name = request.POST.get('last_school_name')
        last_attended_class = request.POST.get('last_attended_class')
        last_school_affiliated_to = request.POST.get('last_school_affiliated_to')

        # Create Lead
        lead = Lead.objects.create(
            school = a1,
            admission_class=admission_class,
            source=source_obj,
            referred_by=referred_by,

            first_name=first_name,
            last_name=last_name,
            email=email,
            mobile=mobile,
            gender=gender,
            dob=dob,

            mother_name=mother_name,
            mother_qualification=mother_qualification,
            mother_res_address=mother_res_address,
            mother_occupation=mother_occupation,
            mother_official_address=mother_official_address,
            mother_income=mother_income,
            mother_email=mother_email,
            mother_mobile=mother_mobile,

            father_name=father_name,
            father_qualification=father_qualification,
            father_res_address=father_res_address,
            father_occupation=father_occupation,
            father_official_address=father_official_address,
            father_income=father_income,
            father_email=father_email,
            father_mobile=father_mobile,

            nationality=nationality,
            religion=religion,
            category=category,
            aadhar_no=aadhar_no,

            last_school_name=last_school_name,
            last_attended_class=last_attended_class,
            last_school_affiliated_to=last_school_affiliated_to,

            created_by=request.user
        )

        messages.success(request, 'Lead added successfully!')
        return redirect('leads_list')

    return render(request,"add_lead_modal.html",{'classes1':classes1,'sources':sources})
    

from django.shortcuts import render, get_object_or_404, redirect
from .models import Lead, LeadSource, LeadStatus, Teacher

def edit_lead(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    a1 = SchoolDetails.objects.get(custid=request.user)
    classes1 = Class.objects.filter(school=a1).order_by('name').distinct()
    aaaa = LeadSource.objects.filter(school=a1).order_by('name').distinct()

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'update':
            lead.first_name = request.POST.get('first_name')
            lead.last_name = request.POST.get('last_name')
            lead.email = request.POST.get('email')
            lead.mobile = request.POST.get('mobile')
            lead.gender = request.POST.get('gender')
            lead.dob = request.POST.get('dob')
            lead.referred_by = request.POST.get('referred_by')
            lead.admission_class = request.POST.get('admission_class')
            lead.source_id = request.POST.get('source') or None
            lead.status_id = request.POST.get('status') or None
            lead.remark = request.POST.get('remark')
            lead.scheduled_at = request.POST.get('scheduled_at') or None
            lead.save()
            return redirect('leads_list')  # Replace with your actual list view name

        elif action == 'delete':
            lead.delete()
            return redirect('leads_list')  # Replace with your actual list view name

    sources = LeadSource.objects.all()
    statuses = LeadStatus.objects.all()
    return render(request, 'lead_edit.html', {
        'lead': lead,
        'sources': sources,
        'statuses': statuses,
        'classes1' : classes1,
        'a1':a1,
        'aaaa': aaaa
    })
    


def transport_fee_view(request):
    a1 = SchoolDetails.objects.get(custid=request.user)

    if request.method == 'POST':
        distance = request.POST.get('distance')
        fee = request.POST.get('fee')

        if distance and fee:
            TransportFee.objects.create(distance=distance, fee=fee, school=a1)
            return redirect('transport_fee_view')  # Redirect to avoid resubmission

    return render(request, 'transport_fee_form.html',{'a1':a1})


def create_timetable(request):
    a1 = SchoolDetails.objects.get(custid=request.user)
    classes = Class.objects.filter(school=a1)
    subjects = Subject.objects.filter(school=a1)
    teachers = Teacher.objects.filter(school=a1)
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

    if request.method == 'POST':
        class_id = request.POST['class_id']
        section_id = request.POST['section_id']

        for day in days:
            for period_num in range(1, 9):
                subject_id = request.POST.get(f"{day}_period_{period_num}_subject")
                teacher_id = request.POST.get(f"{day}_period_{period_num}_teacher")

                if subject_id and teacher_id:
                    TimeTableEntry.objects.update_or_create(
                        school = a1,
                        class_name_id=class_id,
                        section_id=section_id,
                        weekday=day,
                        period=f'Period {period_num}',
                        defaults={
                            'subject_id': subject_id,
                            'teacher_id': teacher_id
                        }
                    )

        messages.success(request, "Time Table saved successfully.")
        return redirect('create_timetable')
        

    return render(request, 'create_timetable.html', {
        'classes': classes,
        'subjects': subjects,
        'teachers': teachers,
        'periods': range(1, 9),
        'days': days,
        'a1':a1
    })

def get_subjects(request):
    """
    AJAX request to get subjects by class ID.
    """
    class_id = request.GET.get('class_id')

    if class_id:
        subjects = Subject.objects.filter(class_assigned_id=class_id).values('id', 'name')
    else:
        subjects = []

    return JsonResponse({'subjects': list(subjects)})

def get_teachers_by_subject(request):
    subject_id = request.GET.get('subject_id')
    if subject_id:
        teachers = Teacher.objects.filter(assigned_subjects1__id=subject_id).values('id', 'first_name', 'last_name')
    else:
        teachers = []

    return JsonResponse({'teachers': list(teachers)})


def get_timetable_data(request):
    class_id = request.GET.get('class_id')
    section_id = request.GET.get('section_id')
    school = SchoolDetails.objects.get(custid=request.user)

    timetable = TimeTableEntry.objects.filter(
        school=school,
        class_name_id=class_id,
        section_id=section_id
    )

    data = {}
    for entry in timetable:
        key = f"{entry.weekday}_period_{entry.period.split()[-1]}"
        data[key] = {
            'subject_id': entry.subject.id,
            'teacher_id': entry.teacher.id
        }

    return JsonResponse({'entries': data})



def teacher_timetable(request):
    teacher = Teacher.objects.get(custid=request.user)
    timetable_entries = TimeTableEntry.objects.filter(teacher=teacher)

    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    period_numbers = [f'Period {i}' for i in range(1, 9)]

    timetable_matrix = []
    for day in days:
        row = []
        for period in period_numbers:
            # find matching entry or None
            entry = next((e for e in timetable_entries if e.weekday == day and e.period == period), None)
            row.append(entry)
        timetable_matrix.append({'day': day, 'periods': row})

    return render(request, 'teacher_timetable.html', {
        'timetable_matrix': timetable_matrix,
        'period_numbers': period_numbers,
    })



def student_timetable(request):
    student = studentadmission.objects.get(custid=request.user)
    timetable_entries = TimeTableEntry.objects.filter(
        class_name=student.classs,
        section=student.section
    )

    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    period_numbers = [f'Period {i}' for i in range(1, 9)]

    timetable_matrix = []
    for day in days:
        row = []
        for period in period_numbers:
            entry = next((e for e in timetable_entries if e.weekday == day and e.period == period), None)
            row.append(entry)
        timetable_matrix.append({'day': day, 'periods': row})

    return render(request, 'student_timetable.html', {
        'timetable_matrix': timetable_matrix,
        'period_numbers': period_numbers,
    })




import requests
from bs4 import BeautifulSoup
from django.shortcuts import render

def fetch_admissions_data():
    
    url = "https://idpscherukupalli.com/admissions/"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for request errors
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Example: Extract table data (adjust selectors based on webpage structure)
        admissions = []
        table = soup.find('table')  # Adjust if data is in a different HTML element
        if table:
            rows = table.find_all('tr')
            for row in rows[1:]:  # Skip header row
                cols = row.find_all('td')
                if cols:
                    admission = {
                        'sno': cols[0].text.strip(),
                        'parentname': cols[1].text.strip(),
                        'childname': cols[2].text.strip(),
                        'mobilenumber': cols[3].text.strip(),
                        'email': cols[4].text.strip(),
                        'location': cols[5].text.strip(),
                        'grade': cols[6].text.strip(),
                        'date': cols[7].text.strip(),
                       
                    }
                    admissions.append(admission)
        return admissions
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return []

def admissions_view(request):
    try:
        a1 = SchoolDetails.objects.get(custid=request.user)
    except SchoolDetails.DoesNotExist:
        messages.error(request, "School details not found!")
        return redirect('admin_dashboard')
    admissions_data = fetch_admissions_data()
    return render(request, 'admissions.html', {'admissions': admissions_data,'a1':a1})
