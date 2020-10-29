from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.serializers import serialize
import datetime


class User(AbstractUser):
    pass


class Assignement_type(models.Model):
    Assignement_type = models.CharField(max_length=100)


class Course(models.Model):
    course_user = models.ForeignKey(User, on_delete=models.CASCADE)
    course_title = models.CharField(
        default="Study Hall", max_length=50, blank=False)
    course_type = models.CharField(max_length=2, default="CP", blank=False)
    course_length = models.CharField(max_length=2, default="FY", blank=False)
    course_teacher = models.CharField(max_length=50, blank=True)
    course_email = models.EmailField(blank=True)
    course_room = models.CharField(max_length=10, blank=True)
    course_enrolled = models.BooleanField(default=True)

    def serialize(self):
        return{
            "id": self.id,
            "user": self.course_user.username,
            "title": self.course_title,
            "type": self.course_type,
            "durration": self.course_length,
            "teacher": self.course_teacher,
            "email": self.course_email,
            "room": self.course_room,
            "enrolled": self.course_enrolled
        }


class Assignments(models.Model):
    Assignment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    Assignment_title = models.CharField(max_length=40, blank=False)
    Assignment_type = models.CharField(
        max_length=15, blank=False, default="Homework")
    Assignment_course = models.ForeignKey(Course, on_delete=models.CASCADE)
    Assignment_due = models.DateField(blank=False)
    Assignemnt_assigned = models.DateField(default=datetime.datetime.now())
    Assignmnet_status = models.BooleanField(default=False)

    def serialize(self):
        return{
            "id": self.id,
            "user": self.Assignment_user.username,
            "title": self.Assignment_title,
            "type": self.Assignment_type,
            "course": self.Assignment_course.course_title,
            "due": self.Assignment_due,
            "given": self.Assignemnt_assigned,
            "status": self.Assignmnet_status
        }
