"""timetable3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from webapp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Homepage, name='HOMES'),
    path('Room-Wise_Search/', search_room_wise, name='rooms'),
    path('Faculty-Wise_Search/', search_faculty_wise, name='faculty'),
    path('Course-Wise_Search/', search_course_wise, name='courses'),

    path('Admin-Panel/', admin_homepage, name="check"),
    path('Search_old_faculty_timetable', check_old, name="old_timetable"),
    path('Create_Faculty/', faculty_create, name="fcreate"),
    path('Update_Faculty/<id>/', faculty_update, name="fupdate"),
    path('Delete_Faculty/<id>/', fac_del, name="fdelete"),
    path('Create_Academic_Year/', create_acad, name="acreate"),
    path('Update_Academic_Year/<id>/', update_acad, name="aupdate"),
    path('Delete_Academic_Year/<id>/', delete_acd, name="adelete"),
    path('Update_Semester/<id>/', update_sem, name="usem"),
    path('Create_Class', create_class, name="cclass"),
    path('Update_Class/<id>/', update_class, name="uclass"),
    path('Delete_Class/<id>/', del_class, name="dclass"),
    path('Create_Table/<id>', create_timetable2, name="ctable"),
    path('Update_Timetable/<id>/', update_table2, name="utable"),
    path('Delete_Timetable/<id>/', del_table2, name="dtable"),
    path('load_semester/', load_sem, name="ajax_load_semester"),
    path('Login_User/', log, name="lg"),
    path('Logout_User/', logout_user, name="logo"),

]
