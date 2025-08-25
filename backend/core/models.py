from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """
    Custom user model that extends Django's AbstractUser.
    This allows for future customization of user fields.
    """
    # Add additional fields here in the future, e.g.:
    # bio = models.TextField(blank=True)
    # profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)
    pass

    def __str__(self):
        return self.username

class Course(models.Model):
    """
    Represents a course in the learning platform.
    """
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Lesson(models.Model):
    """
    Represents a single lesson within a course.
    """
    title = models.CharField(max_length=255)
    content = models.TextField(help_text="The main content of the lesson.")
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0, help_text="The order of the lesson within the course.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.course.title}: {self.title}"
