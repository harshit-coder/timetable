from django.forms import ModelForm
from django import forms
from django.forms import ModelChoiceField
from .models import *
from django.core import validators
from .views import *
from crispy_forms.helper import FormHelper
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class room_search(forms.Form):
    fields = 'room'
    room = forms.ModelChoiceField(queryset=room_no.objects.all(),
                                  widget=forms.Select(attrs={'class': "form-control", 'placeholder': "Choose",
                                                             'style': "background-color: #dadada"}), required=True)


class faculty_search(forms.Form):
    fields = 'faculty'
    faculty = forms.ModelChoiceField(queryset=faculty.objects.all(),
                                     widget=forms.Select(attrs={'class': "form-control", 'placeholder': "Choose",
                                                                'style': "background-color: #dadada"}), required=True)


class course_search(forms.Form):
    fields = ('CourseName', 'Sem')
    CourseName = forms.ModelChoiceField(queryset=Course.objects.all(),
                                        widget=forms.Select(attrs={'class': "form-control", 'placeholder': "Choose",
                                                                   'style': "background-color: #dadada"}),
                                        required=True)

    Sem = forms.ModelChoiceField(queryset=sem.objects.filter(show1=True),
                                 widget=forms.Select(attrs={'class': "form-control", 'placeholder': "Choose",
                                                            'style': "background-color: #dadada"}),
                                 required=True)


class findlast_form(forms.Form):
    fields = ('faculty', 'Year', 'Sem')
    faculty = forms.ModelChoiceField(queryset=faculty.objects.all(),
                                     widget=forms.Select(attrs={'class': "form-control", 'placeholder': "Choose",
                                                                }), required=True)
    Year = forms.ModelChoiceField(queryset=year.objects.all(),
                                  widget=forms.Select(attrs={'class': "form-control", 'placeholder': "Choose",
                                                             }), required=True)
    Sem = forms.ChoiceField(choices=TICK_CHOICES,
                            widget=forms.Select(attrs={'class': "form-control", 'placeholder': "Choose",
                                                       }), required=True)


class course_form(forms.ModelForm):
    class Meta:
        model = table1
        fields = '__all__'


class timetable_form1(forms.ModelForm):
    helper = FormHelper()
    helper.form_show_labels = False

    class Meta:
        model = table1

        fields = ('academic_year1', 'course_name', 'part1', 'sem1')
        academic_year1 = forms.ModelChoiceField(queryset=year.objects.all(),
                                                widget=forms.Select(
                                                    attrs={'class': "form-control", 'placeholder': "Choose",
                                                           }),
                                                required=True)
        course_name = forms.ModelChoiceField(queryset=Course.objects.all(),
                                             widget=forms.Select(
                                                 attrs={'class': "form-control", 'placeholder': "Choose",
                                                        }),
                                             required=True)
        part1 = forms.ChoiceField(choices=PART_CHOICES,
                                  widget=forms.Select(attrs={'class': "form-control", 'placeholder': "Choose",
                                                             }), required=True)

        sem1 = forms.ModelChoiceField(queryset=sem.objects.filter(show1=True),
                                      widget=forms.Select(attrs={'class': "form-control", 'placeholder': "Choose",
                                                                 }),
                                      required=True)


class timetable_form2(forms.ModelForm):
    helper = FormHelper()
    helper.form_show_labels = False

    class Meta:
        model = table2
        fields = ('day', 'section_type', 'Lecture_type', 'time', 'paper_name1', 'paper_code1', 'faculty_name1',
                  'faculty_name2', 'room1')


class sem_form(forms.ModelForm):
    class Meta:
        model = sem
        fields = '__all__'


class acad_form(forms.ModelForm):
    class Meta:
        model = year
        fields = '__all__'


class facul_form(forms.ModelForm):
    class Meta:
        model = faculty
        fields = '__all__'


class search_form1(forms.Form):
    fields = ('acad_yr', 'CourseName', 'Sem')
    acad_yr = forms.ModelChoiceField(queryset=year.objects.all(),
                                     widget=forms.Select(attrs={'class': "form-control", 'placeholder': "Choose",
                                                                }),
                                     required=True)
    CourseName = forms.ModelChoiceField(queryset=Course.objects.all(),
                                        widget=forms.Select(attrs={'class': "form-control", 'placeholder': "Choose",
                                                                   }),
                                        required=True)

    Sem = forms.ModelChoiceField(queryset=sem.objects.all(),
                                 widget=forms.Select(attrs={'class': "form-control", 'placeholder': "Choose",
                                                            }),
                                 required=True)


class user_form(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class login_form(forms.Form):
    fields = ['Username', 'Password']

    Username = forms.CharField(max_length=200,
                               widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "Enter Username",
                                                             }), required=True)
    Password = forms.CharField(max_length=200, widget=forms.PasswordInput(
        attrs={'class': "form-control", 'placeholder': "Enter password",
               }), required=True)
