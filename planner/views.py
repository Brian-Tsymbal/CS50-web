import json
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from django.db import IntegrityError
from django.db.models import Avg, Max, Min, Sum
from django.core.exceptions import ObjectDoesNotExist


from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


from .models import User, Course, Assignments
from .forms import CourseForm, Assignment_type_list, AssignmentForm

# pages


def index(request):
    # Authenticated users credentials
    if request.user.is_authenticated:
        return render(request, "planner/index.html", {
            "courses": Course.objects.filter(course_user=request.user, course_enrolled=True),
            "Assignments": Assignments.objects.filter(Assignment_user=request.user, Assignmnet_status=False).order_by("Assignment_due")
        })

    # Everyone else is prompted to sign in
    else:
        return HttpResponseRedirect(reverse("login"))


@ login_required
@ csrf_exempt
def create(request):
    return render(request, "planner/create.html", {
        "CourseForm": CourseForm(),
        "AssignmentForm": AssignmentForm(),
        "courses": Course.objects.filter(
            course_user=request.user, course_enrolled=True)
    })


# assignemnts

def CreateAssignment(request):
    forms = AssignmentForm(request.POST)
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    else:
        if forms.is_valid():
            try:
                title = request.POST['NewAssignment_Title']
                form = request.POST['NewAssignment_Form']
                course = forms.cleaned_data['NewAssignment_Course']
                CourseTitle = Course.objects.get(course_title=course)
                DueDate = request.POST['NewAssignment_DueDate']
                Assignment = Assignments(Assignment_user=request.user, Assignment_title=title,
                                         Assignment_type=form, Assignment_course=CourseTitle, Assignment_due=DueDate)
                Assignment.save()
                return HttpResponseRedirect(reverse("index"))
            except ObjectDoesNotExist:
                return render(request, "planner/create.html", {
                    "CourseForm": CourseForm(),
                    "AssignmentForm": AssignmentForm(initial={
                        'NewAssignment_Title': title,
                        'NewAssignment_Form': form,
                        'NewAssignment_Course': "",
                    }),
                    "courses": Course.objects.filter(
                        course_user=request.user, course_enrolled=True),
                    "error": "You do not belong to this course, please check your spelling."
                })


@ login_required
def AssignmentAll(request):
    assignment = Assignments.objects.filter(Assignment_user=request.user)
    assignment = reversed(assignment.order_by("-Assignment_due").all())
    return JsonResponse([assignment.serialize() for assignment in assignment], safe=False)


@ csrf_exempt
@ login_required
def Assignment(request, Assignment_id):
    try:
        assignment = Assignments.objects.get(
            Assignment_user=request.user, pk=Assignment_id)
    except Assignments.DoesNotExist:
        return JsonResponse({"error": "Assignment not found."}, status=404)

    if request.method == "GET":
        return JsonResponse(assignment.serialize(), safe=False)

    elif request.method == "PUT":
        data = json.loads(request.body)
        print("initiated")
        if data.get("status") is not None:
            assignment.Assignmnet_status = data["status"]
        assignment.save()
        return JsonResponse(assignment.serialize(), safe=False)

    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)


# courses

def CreateCourse(request):
    forms = CourseForm(request.POST)
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    else:
        if forms.is_valid():
            title = request.POST["NewCourse_Title"]
            form = request.POST["NewCourse_Type"]
            length = request.POST["NewCourse_Length"]
            teacher = request.POST["NewCourse_Teacher"]
            email = request.POST["NewCourse_Email"]
            room = request.POST["Newcourse_Location"]
            Courses = Course(course_user=request.user, course_title=title,
                             course_type=form, course_length=length, course_teacher=teacher, course_email=email, course_room=room)
            Courses.save()
            return HttpResponseRedirect(reverse("course"))


@login_required
def CourseAll(request):
    course = Course.objects.filter(course_user=request.user)
    return JsonResponse([course.serialize() for course in course], safe=False)


@csrf_exempt
@login_required
def course(request, course_id):
    try:
        course = Course.objects.get(course_user=request.user, pk=course_id)
    except course.DoesNotExist:
        return JsonResponse({"error": "Course not found."}, status=404)

    if request.method == "GET":
        return JsonResponse(course.serialize(), safe=False)

    elif request.method == "PUT":
        data = json.loads(request.body)
        print("initiated")
        if data.get("enrolled") is not None:
            course.course_enrolled = data["enrolled"]
            course.delete()
        return JsonResponse(course.serialize(), safe=False)

    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)


@login_required
def CourseList(request):
    return render(request, "planner/courses.html", {
        "Courses": Course.objects.filter(course_user=request.user)})


# bootstrap

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "planner/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "planner/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "planner/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "planner/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "planner/register.html")
