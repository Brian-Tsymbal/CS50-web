from django.contrib import admin

# Register your models here.
from .models import User, Course, Assignments

admin.site.register(User),
admin.site.register(Course),
admin.site.register(Assignments),
