from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Course, Enrollment
from django.contrib.auth import login
from django.contrib.auth.views import LogoutView
from .forms import SignupForm
from .forms import CourseForm
from django.contrib import messages
from .models import StudentProfile
def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            return redirect("dashboard")  
    else:
        form = SignupForm()
    return render(request, "courses/signup.html", {"form": form})


def dashboard(request):
    return render(request, "courses/dashboard.html")


def home(request):
    return render(request, "courses/home.html")


@login_required
def course_list(request):
    courses = Course.objects.all()
    enrolled = Enrollment.objects.filter(student=request.user.studentprofile).values_list("course_id", flat=True) if request.user.role == "student" else []
    return render(request, "courses/course_list.html", {"courses": courses, "enrolled": enrolled})


@login_required
def enroll_course(request, course_id):
    if request.user.role != "student":
        return redirect("course_list")  # only students can enroll
    
    course = get_object_or_404(Course, id=course_id)
    student = request.user.studentprofile

    # prevent duplicate enrollment
    Enrollment.objects.get_or_create(student=student, course=course)

    return redirect("course_list")


@login_required
def create_course(request):
    if request.user.role != "instructor":
        return redirect("home")  # only instructors allowed
    
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user.instructorprofile
            course.save()
            return redirect("instructor_courses")
    else:
        form = CourseForm()
    return render(request, "courses/create_course.html", {"form": form})


@login_required
def instructor_courses(request):
    if request.user.role != "instructor":
        return redirect("home")
    
    courses = Course.objects.filter(instructor=request.user.instructorprofile)
    return render(request, "courses/instructor_courses.html", {"courses": courses})



@login_required
def course_students(request, course_id):
    if request.user.role != "instructor":
        return redirect("home")

    course = Course.objects.get(id=course_id, instructor=request.user.instructorprofile)
    enrollments = Enrollment.objects.filter(course=course).select_related("student__user")

    return render(request, "courses/course_students.html", {"course": course, "enrollments": enrollments})


class CustomLogoutView(LogoutView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return redirect("home")
    
@login_required
def edit_course(request, course_id):
    if request.user.role != "instructor":
        return redirect("home")

    course = get_object_or_404(Course, id=course_id, instructor=request.user.instructorprofile)

    if request.method == "POST":
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, "Course updated successfully!")
            return redirect("instructor_courses")
    else:
        form = CourseForm(instance=course)

    return render(request, "courses/edit_course.html", {"form": form, "course": course})


@login_required
def delete_student(request, student_id):
    if request.user.role != "instructor":
        return redirect("home")

    # Only delete if the student is enrolled in this instructor’s courses
    student_profile = get_object_or_404(StudentProfile, id=student_id)

    # Check if this student is enrolled in any course of the instructor
    instructor_courses = Course.objects.filter(instructor=request.user.instructorprofile)
    if Enrollment.objects.filter(student=student_profile, course__in=instructor_courses).exists():
        student_profile.delete()  #  triggers signal to remove enrollments & progress

    return redirect("instructor_courses")