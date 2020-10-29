from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path("record", views.create, name="create"),
    path("courses", views.CourseList, name="course"),



    path("NewAssignment", views.CreateAssignment, name="NewAssignment"),
    path("AllAssignment", views.AssignmentAll, name="AllAssignment"),
    path("AllAssignment/<int:Assignment_id>",
         views.Assignment, name="Assignment"),

    path("NewCourse", views.CreateCourse, name="NewCourse"),
    path("AllCourses", views.CourseAll, name="AllCourses"),
    path("AllCourses/<int:course_id>", views.course, name="course"),

]
