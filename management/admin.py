from django.contrib import admin
from .models import Student, Faculty, Course, Department, Enrollment, UserProfile

admin.site.register(Student)
admin.site.register(Faculty)
admin.site.register(Course)
admin.site.register(Department)
admin.site.register(Enrollment)
admin.site.register(UserProfile)