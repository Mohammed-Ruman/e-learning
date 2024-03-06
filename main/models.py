from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

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
