from django import forms
from .models import Student, Faculty, Department, Course, Enrollment

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email', 'date_of_birth', 'enrollment_date']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'enrollment_date': forms.DateInput(attrs={'type': 'date'}),
        }

class FacultyForm(forms.ModelForm):
    class Meta:
        model = Faculty
        fields = ['first_name', 'last_name', 'email', 'department', 'hire_date']
        widgets = {
            'hire_date': forms.DateInput(attrs={'type': 'date'}),
        }

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'head']

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['code', 'title', 'department', 'credits', 'faculty']

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['student', 'course', 'enrollment_date']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-control'}),
            'enrollment_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }


