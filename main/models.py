from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings


User=get_user_model()

# Create your models here.

class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    students = models.ManyToManyField(User, related_name='courses_purchased', blank=True)
    cover_image = models.ImageField(upload_to='course_covers/', null=True, blank=True)
    course_price = models.FloatField()

    def __str__(self):
        return self.title

class CourseContent(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    content_title = models.CharField(max_length=255)
    content = models.FileField(upload_to='course_videos/')

    def __str__(self):
        return self.title

class Subscription(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    purchased = models.BooleanField(default=False)

@receiver(post_save, sender=Course)
def send_course_added_email(sender, instance, created, **kwargs):
    if created:

        courses = Course.objects.filter(teacher=instance.teacher)
        sub=Subscription.objects.filter(course__in=courses, purchased=True)
        student_set = {sup.student for sup in sub}
        # Send an email to each student
        for student in student_set:
            send_mail(
                'New Course Added!',
                'Dear E-Learners, a new course has been added to the platform.',
                settings.EMAIL_HOST,  # Sender's email
                [student.email],  # List of recipients
                fail_silently=False,
            )