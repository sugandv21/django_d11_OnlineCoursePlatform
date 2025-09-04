from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
from .models import StudentProfile, InstructorProfile, Progress, Enrollment


# Auto create profile when user signs up
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == "student":
            StudentProfile.objects.create(user=instance)
        elif instance.role == "instructor":
            InstructorProfile.objects.create(user=instance)

@receiver(post_delete, sender=StudentProfile)
def delete_student_related_data(sender, instance, **kwargs):
    # Delete related enrollments and progress
    enrollments = Enrollment.objects.filter(student=instance)
    Progress.objects.filter(enrollment__in=enrollments).delete()
    enrollments.delete()

    # Also delete the User account so they can't log in again
    if instance.user:
        instance.user.delete()
