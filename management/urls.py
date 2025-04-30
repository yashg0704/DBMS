from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('students/', views.student_list, name='student_list'),
    path('students/add/', views.student_form, name='student_form'),
    path('students/<int:student_id>/update/', views.student_update, name='student_update'),
    path('students/<int:student_id>/delete/', views.student_delete, name='student_delete'),
    path('students/<int:student_id>/', views.student_detail, name='student_detail'),
    
    # Faculty URLs
    path('faculty/', views.faculty_list, name='faculty_list'),
    path('faculty/add/', views.faculty_form, name='faculty_form'),
    path('faculty/<int:faculty_id>/update/', views.faculty_update, name='faculty_update'),
    path('faculty/<int:faculty_id>/delete/', views.faculty_delete, name='faculty_delete'),
    path('faculty/<int:faculty_id>/', views.faculty_detail, name='faculty_detail'),

    # Department URLs
    path('departments/', views.department_list, name='department_list'),
    path('departments/add/', views.department_form, name='department_form'),
    path('departments/<int:department_id>/update/', views.department_update, name='department_update'),
    path('departments/<int:department_id>/delete/', views.department_delete, name='department_delete'),
    path('departments/<int:department_id>/', views.department_detail, name='department_detail'),
    
    # Course URLs
    path('courses/', views.course_list, name='course_list'),
    path('courses/add/', views.course_form, name='course_form'),
    path('courses/<int:course_id>/update/', views.course_update, name='course_update'),
    path('courses/<int:course_id>/delete/', views.course_delete, name='course_delete'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    
    # Enrollment URLs
    path('enrollments/', views.enrollment_list, name='enrollment_list'),
    path('enroll/<int:student_id>/<int:course_id>/', views.enroll_student_in_course, name='enroll_student'),
    path('enrollments/add/', views.enrollment_form, name='enrollment_form'),
    path('enrollments/<int:enrollment_id>/', views.enrollment_detail, name='enrollment_detail'),
    path('enrollments/<int:enrollment_id>/edit/', views.edit_enrollment, name='edit_enrollment'),
    path('enrollments/<int:enrollment_id>/delete/', views.delete_enrollment, name='delete_enrollment'),
]