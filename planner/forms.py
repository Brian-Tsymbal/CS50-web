from django import forms
from .models import User, Course

Course_list = []
Assignment_type_list = [
    ("Homework", "Homework"),
    ("Project", "Project"),
    ("Exam", "Exam")
]
Class_type_list = [
    ("CP", "College Placement"),
    ("H", "Honors"),
    ("AP", "Advanced Placement"),
    ("IB", "International Baccalaureate")
]
Class_length_list = [
    ("FY", "Full Year"),
    ("FS", "First Semester"),
    ("SS", "Second Semester"),
    ("FQ", "First Quarter"),
    ("SQ", "Second Quarter"),
    ("TQ", "Third Quarter"),
    ("fQ", "Fourth Quarter"),
    ("FT", "First Trimester"),
    ("ST", "Second Trimester"),
    ("TT", "Third Trimester")
]


class CourseForm(forms.Form):
    NewCourse_Title = forms.CharField(
        label="*Name of the Class:")
    NewCourse_Type = forms.ChoiceField(
        label="*What is the Class Weight:", choices=Class_type_list)
    NewCourse_Length = forms.ChoiceField(
        label="*How Long is the Class:", choices=Class_length_list)
    NewCourse_Teacher = forms.CharField(
        label="What is Your Teacher's Name:", max_length=50, required=False)
    NewCourse_Email = forms.EmailField(
        label="What is Your Teacher's Email:", required=False)
    Newcourse_Location = forms.CharField(
        label="Room Number", max_length=10, required=False)


class DateInput(forms.DateInput):
    input_type = 'date'


class AssignmentForm(forms.Form):
    NewAssignment_Title = forms.CharField(label="Name of the Assignment:")
    NewAssignment_Form = forms.ChoiceField(
        label="What is the Type of Assignment:", choices=Assignment_type_list)
    NewAssignment_Course = forms.CharField(
        label="An Assignment for What Class:")
    NewAssignment_DueDate = forms.DateField(
        label="Due Date:", widget=DateInput)
