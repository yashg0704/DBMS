from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Student, Faculty, Department, Course, Enrollment
from .forms import StudentForm, FacultyForm, DepartmentForm, CourseForm, EnrollmentForm
from django.db import transaction
from django.http import HttpResponse
from django.http import JsonResponse
from django.db import connection
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import UserProfile
from django.contrib.auth.models import User

def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            role = user.userprofile.role
            if role == 'student':
                return redirect('student_dashboard')
            elif role == 'faculty':
                return redirect('faculty_dashboard')
            elif role == 'admin':
                return redirect('admin_dashboard')
        else:
            return render(request, 'management/login.html', {'error': 'Invalid credentials'})
    return render(request, 'management/login.html')

def user_logout(request):
    logout(request)
    return redirect('login')  # Or redirect to a goodbye page

def no_permission(request):
    return render(request, 'management/no_permission.html')

@login_required
def student_dashboard(request):
    if request.user.userprofile.role != 'student':
        return redirect('no_permission')
    student = Student.objects.get(user=request.user)
    courses = Enrollment.objects.filter(student=student)
    return render(request, 'management/student_dashboard.html', {'student': student, 'courses': courses})

@login_required
def faculty_dashboard(request):
    if request.user.userprofile.role != 'faculty':
        return redirect('no_permission')
    faculty = Faculty.objects.get(user=request.user)
    courses = Course.objects.filter(faculty=faculty)
    return render(request, 'management/faculty_dashboard.html', {'faculty': faculty, 'courses': courses})

@login_required
def admin_dashboard(request):
    if request.user.userprofile.role != 'admin':
        return redirect('no_permission')
    return render(request, 'management/admin_dashboard.html')

def get_student_courses(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    # Call stored procedure
    with connection.cursor() as cursor:
        cursor.callproc('get_student_courses', [student_id])
        courses = cursor.fetchall()  # Fetch (id, title)

    return render(request, 'management/student_courses.html', {
        'student': student,
        'courses': courses
    })

# Home View
def home(request):
    return render(request, 'management/home.html')

# Student Views
def student_list(request):
    students = Student.objects.all()
    return render(request, 'management/student_list.html', {'students': students})

def student_detail(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    enrollments = Enrollment.objects.filter(student=student).select_related('course')
    return render(request, 'management/student_detail.html', {
        'student': student,
        'enrollments': enrollments
    })

def student_form(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            first_name = form.cleaned_data['first_name']
            email = form.cleaned_data['email']
            date_of_birth = form.cleaned_data['date_of_birth']

            # Generate password
            password = first_name[:3].lower() + date_of_birth.strftime('%d-%m-%y')

            # Create user
            user = User.objects.create_user(username=email, email=email, password=password)

            student.user = user
            student.save()

            messages.success(request, f"Student added successfully! Default password: {password}")
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'management/form_template.html', {'form': form, 'title': 'Add Student'})

def student_update(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Student updated successfully!")
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'management/form_template.html', {'form': form, 'title': 'Edit Student'})

def student_delete(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == "POST":
        student.delete()
        messages.success(request, "Student deleted successfully!")
        return redirect('student_list')
    return render(request, 'management/student_confirm_delete.html', {'student': student})

# Faculty Views
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import FacultyForm
from .models import Faculty

def faculty_form(request):
    if request.method == "POST":
        form = FacultyForm(request.POST)
        if form.is_valid():
            faculty = form.save(commit=False)
            first_name = form.cleaned_data['first_name']
            email = form.cleaned_data['email']
            hire_date = form.cleaned_data['hire_date']

            # Generate password
            password = first_name[:3].lower() + hire_date.strftime('%d-%m-%y')

            # Create user
            user = User.objects.create_user(username=email, email=email, password=password)

            faculty.user = user
            faculty.save()

            # No need to manually create the UserProfile here
            # The signal will automatically create the profile with role='faculty'

            messages.success(request, f"Faculty member added successfully! Default password: {password}")
            return redirect('faculty_list')
    else:
        form = FacultyForm()
    return render(request, 'management/faculty_form.html', {'form': form, 'title': 'Add Faculty'})

def faculty_list(request):
    faculties = Faculty.objects.all()
    print(f"Faculty count: {faculties.count()}")  # Add this for debugging
    return render(request, 'management/faculty_list.html', {'faculties': faculties})

def faculty_detail(request, faculty_id):
    faculty = get_object_or_404(Faculty, id=faculty_id)
    courses = Course.objects.filter(faculty=faculty)
    return render(request, 'management/faculty_detail.html', {
        'faculty': faculty,
        'courses': courses
    })

def faculty_update(request, faculty_id):
    faculty = get_object_or_404(Faculty, id=faculty_id)
    if request.method == "POST":
        form = FacultyForm(request.POST, instance=faculty)
        if form.is_valid():
            form.save()
            messages.success(request, "Faculty updated successfully!")
            return redirect('faculty_list')
    else:
        form = FacultyForm(instance=faculty)
    return render(request, 'management/form_template.html', {'form': form, 'title': 'Edit Faculty'})

def faculty_delete(request, faculty_id):
    faculty = get_object_or_404(Faculty, id=faculty_id)
    if request.method == "POST":
        faculty.delete()
        messages.success(request, "Faculty deleted successfully!")
        return redirect('faculty_list')
    return render(request, 'management/faculty_confirm_delete.html', {'faculty': faculty})

# Department Views
def department_form(request):
    if request.method == "POST":
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Department added successfully!")
            return redirect('department_list')
    else:
        form = DepartmentForm()
    return render(request, 'management/form_template.html', {'form': form, 'title': 'Add Department'})

def department_list(request):
    departments = Department.objects.all()
    return render(request, 'management/department_list.html', {'departments': departments})

def department_detail(request, department_id):
    department = get_object_or_404(Department, id=department_id)
    # Changed variable name to match template
    faculty_members = Faculty.objects.filter(department=department)
    return render(request, 'management/department_detail.html', {
        'department': department,
        'faculty_members': faculty_members  # Changed from 'faculties' to 'faculty_members'
    })

def department_update(request, department_id):
    department = get_object_or_404(Department, id=department_id)
    if request.method == "POST":
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            messages.success(request, "Department updated successfully!")
            return redirect('department_list')
    else:
        form = DepartmentForm(instance=department)
    return render(request, 'management/form_template.html', {'form': form, 'title': 'Edit Deparment'})

def department_delete(request, department_id):
    department = get_object_or_404(Department, id=department_id)
    if request.method == "POST":
        department.delete()
        messages.success(request, "Department deleted successfully!")
        return redirect('department_list')
    return render(request, 'management/department_confirm_delete.html', {'department': department})

# Course Views
def course_form(request):
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Course added successfully!")
            return redirect('course_list')
    else:
        form = CourseForm()
    return render(request, 'management/form_template.html', {'form': form, 'title': 'Add Course'})

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'management/course_list.html', {'courses': courses})

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    enrollments = Enrollment.objects.filter(course=course).select_related('student')  # Get enrollments with student info
    return render(request, 'management/course_detail.html', {
        'course': course,
        'enrollments': enrollments,
    })

def course_update(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == "POST":
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, "Course updated successfully!")
            return redirect('course_list')
    else:
        form = CourseForm(instance=course)
    return render(request, 'management/form_template.html', {'form': form, 'title': 'Edit Course'})

def course_delete(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == "POST":
        course.delete()
        messages.success(request, "Course deleted successfully!")
        return redirect('course_list')
    return render(request, 'management/course_confirm_delete.html', {'course': course})

# Enrollment Views

def enrollment_form(request):
    if request.method == "POST":
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Enrollment completed successfully!")
            return redirect('enrollment_list')
    else:
        form = EnrollmentForm()
    return render(request, 'management/form_template.html', {'form': form, 'title': 'Enroll Student'})

def enrollment_list(request):
    enrollments = Enrollment.objects.all()
    return render(request, 'management/enrollment_list.html', {'enrollments': enrollments})

def enrollment_detail(request, enrollment_id):
    enrollment = get_object_or_404(Enrollment, id=enrollment_id)
    return render(request, 'management/enrollment_detail.html', {'enrollment': enrollment})

def edit_enrollment(request, enrollment_id):
    enrollment = get_object_or_404(Enrollment, id=enrollment_id)
    if request.method == "POST":
        form = EnrollmentForm(request.POST, instance=enrollment)
        if form.is_valid():
            form.save()
            messages.success(request, "Enrollment updated successfully!")
            return redirect('enrollment_list')
    else:
        form = EnrollmentForm(instance=enrollment)
    return render(request, 'management/form_template.html', {'form': form, 'title': 'Edit Enrollment'})

def delete_enrollment(request, enrollment_id):
    enrollment = get_object_or_404(Enrollment, id=enrollment_id)
    
    if request.method == "POST":
        enrollment.delete()
        messages.success(request, "Enrollment deleted successfully!")
        return redirect('enrollment_list')

    return render(request, 'management/enrollment_confirm_delete.html', {'enrollment': enrollment})

def enroll_student_in_course(request, student_id, course_id):
    try:
        with transaction.atomic():
            student = get_object_or_404(Student, id=student_id)
            course = get_object_or_404(Course, id=course_id)

            # Prevent duplicate enrollments
            if Enrollment.objects.filter(student=student, course=course).exists():
                messages.warning(request, "Student is already enrolled in this course!")
                return redirect('course_list')

            Enrollment.objects.create(student=student, course=course)
            messages.success(request, f"{student.first_name} enrolled in {course.title} successfully!")
            return redirect('course_list')

    except Exception as e:
        messages.error(request, f"Enrollment failed: {str(e)}")
        return redirect('course_list')