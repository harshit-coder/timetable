from django.contrib import admin

from import_export.admin import ImportExportModelAdmin
# Register your models here.
from webapp.models import *
from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget

from django.contrib.auth.admin import UserAdmin


class table2admin(admin.TabularInline):
    model = table2


class table1admin(admin.ModelAdmin):
    inlines = [table2admin]

    class Meta:
        model = table1


class paper_admin(admin.TabularInline):
    model = paper


class course_admin(admin.ModelAdmin):
    inlines = [paper_admin]

    class Meta:
        model = paper


admin.site.register(section)

admin.site.register(Course, course_admin)


@admin.register(year)
class year_admin(admin.ModelAdmin):
    list_display = ['academic_year', 'show']


@admin.register(room_no)
class room_noadmin(ImportExportModelAdmin):
    list_display = ['room']


admin.site.register(table1, table1admin)


@admin.register(faculty)
class faculty_admin(ImportExportModelAdmin):
    list_display = ['faculty_name', 'faculty_code']
    search_fields = ('faculty_name', 'faculty_code')


admin.site.register(User_data)


@admin.register(sem)
class semadmin(admin.ModelAdmin):
    list_display = ['semester', 'show1']


@admin.register(Lecture)
class lecture_admin(admin.ModelAdmin):
    list_display = ['Lecture_type', 'Lecture_type_ff']
    search_fields = ('Lecture_type', 'Lecture_type_ff')
