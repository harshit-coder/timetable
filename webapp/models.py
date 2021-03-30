from django.db import models
from django.core.exceptions import ValidationError

DAYS_CHOICES = [
    ('MONDAY', 'Monday'),
    ('TUESDAY', 'Tuesday'),
    ('WEDNESDAY', 'Wednesday'),
    ('THURSDAY', 'Thursday'),
    ('FRIDAY', 'Friday'),
    ('SATURDAY', 'Saturday'),

]
TICK_CHOICES = [
    ('Checked Semesters', 'Checked Semesters'),
    ('Unchecked Semesters', 'Unchecked Semesters'),

]

SEM_CHOICES = [
    ('1st', '1st'),
    ('2nd', '2nd'),
    ('3rd', '3rd'),
    ('4th', '4th'),
    ('5th', '5th'),
    ('6th', '6th'),
    ('7th', '7th'),
    ('8th', '8th'),
    ('9th', '9th'),
    ('10th', '10th'),
]

PART_CHOICES = [
    ('1st', '1st'),
    ('2nd', '2nd'),
    ('3rd', '3rd'),
    ('4th', '4th'),
    ('5th', '5th'),

]

TIME_CHOICES = [
    ('08.30 TO 09.30', '08.30 TO 09.30'),
    ('09.30 TO 10.30', '09.30 TO 10.30'),
    ('10.30 TO 11.30', '10.30 TO 11.30'),
    ('11.30 TO 12.30', '11.30 TO 12.30'),
    ('12.30 TO 01.30', '12.30 TO 01.30'),
    ('01.30 TO 02.30', '01.30 TO 02.30'),
    ('02.30 TO 03.30', '02.30 TO 03.30'),
    ('03.30 TO 04.30', '03.30 TO 04.30'),
    ('04.30 TO 05.30', '04.30 TO 05.30'),

]


class section(models.Model):
    section_type = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.section_type


class Lecture(models.Model):
    Lecture_type = models.CharField(max_length=100, default="TH", verbose_name="Lecture code")
    Lecture_type_ff = models.CharField(max_length=100, default="Theory", verbose_name="Lecture Name")

    def __str__(self):
        return str(self.Lecture_type_ff)


class room_no(models.Model):
    room = models.CharField(max_length=100, default="1", unique=True)

    def __str__(self):
        return str(self.room)


class faculty(models.Model):
    faculty_name = models.CharField(max_length=200, default="Name", null=True)
    faculty_code = models.CharField(max_length=100, default="CODE")

    def __str__(self):
        return str(self.faculty_name)


class Course(models.Model):
    course_code = models.CharField(max_length=10, default="CODE", unique=True)
    course_name = models.CharField(max_length=200, default="Name", unique=True)

    def __str__(self):
        return str(self.course_name)


class paper(models.Model):
    Course_name = models.ForeignKey('Course', on_delete=models.CASCADE)
    paper_name = models.CharField(max_length=200, default="Science")
    paper_code = models.CharField(max_length=30, default="0123")

    def __str__(self):
        return str(self.paper_name)


class sem(models.Model):
    semester = models.CharField(max_length=100, choices=SEM_CHOICES, default='1st', null=True,
                                verbose_name="Choose Semester")
    show1 = models.BooleanField(verbose_name="Tick if this is the current going semester")

    def __str__(self):
        return str(self.semester)


class year(models.Model):
    academic_year = models.CharField(max_length=100, default="2019-20", verbose_name="Academic Year")
    show = models.BooleanField(verbose_name="Tick if this is the current year")

    def __str__(self):
        return str(self.academic_year)


class table1(models.Model):
    academic_year1 = models.ForeignKey('year', on_delete=models.CASCADE, null=True, verbose_name="Select Academic Year")
    course_name = models.ForeignKey('Course', on_delete=models.CASCADE, null=True, verbose_name="Choose Course")
    part1 = models.CharField(max_length=100, choices=PART_CHOICES, default='1st', null=True, verbose_name="Part")
    sem1 = models.ForeignKey('sem', on_delete=models.CASCADE, null=True, verbose_name="Semester")

    def __str__(self):
        return str(self.academic_year1.academic_year+"--" + self.course_name.course_name+"--" + self.part1 + " year"+"--" + self.sem1.semester + " sem")


class table2(models.Model):
    choose = models.ForeignKey('table1', on_delete=models.CASCADE, blank=True, verbose_name="Choose faculty1")

    day = models.CharField(max_length=100, choices=DAYS_CHOICES, null=True, blank=True, verbose_name="Choose day")
    section_type = models.ForeignKey('section', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Section")
    Lecture_type = models.ForeignKey('Lecture', on_delete=models.CASCADE, null=True, blank=True,
                                     verbose_name="Lecture Type")
    time = models.CharField(max_length=100, choices=TIME_CHOICES, null=True, blank=True, verbose_name="Choose time")
    paper_name1 = models.CharField(max_length=200, blank=True, verbose_name="Enter paper name")
    paper_code1 = models.CharField(max_length=200, blank=True, verbose_name="Enter paper code")
    faculty_name1 = models.ForeignKey('faculty', on_delete=models.CASCADE, null=True, blank=True, related_name='fac1',
                                      verbose_name="Choose faculty1")
    faculty_name2 = models.ForeignKey('faculty', on_delete=models.CASCADE, null=True, blank=True, related_name='fac2',
                                      verbose_name="Choose faculty2(for lab)")
    room1 = models.ForeignKey('room_no', on_delete=models.CASCADE, null=True, blank=True, related_name='rom1',
                              verbose_name="Choose the room")

    def __str__(self):
        return str(self.paper_name1)


class sem_fac(models.Model):
    semester2 = models.CharField(max_length=100, choices=SEM_CHOICES, default='1st', null=True,
                                 verbose_name="Choose Semester")
    show12 = models.BooleanField(verbose_name="Tick which you want to show to students")

    def __str__(self):
        return str(self.semester2)


class User_data(models.Model):
    username = models.CharField(max_length=200, default="username")
    password = models.CharField(max_length=200, default="Password")
