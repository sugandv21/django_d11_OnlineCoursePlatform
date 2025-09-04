from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("signup/", views.signup_view, name="signup"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("login/", auth_views.LoginView.as_view(template_name="courses/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="home"), name="logout"),

    path("courses/", views.course_list, name="course_list"),
    path("courses/enroll/<int:course_id>/", views.enroll_course, name="enroll_course"),
    
    path("instructor/courses/", views.instructor_courses, name="instructor_courses"),
    path("instructor/courses/create/", views.create_course, name="create_course"),
    path("instructor/courses/<int:course_id>/students/", views.course_students, name="course_students"),
    path("instructor/courses/<int:course_id>/edit/", views.edit_course, name="edit_course"),
    path("instructor/students/delete/<int:student_id>/", views.delete_student, name="delete_student"),


]
