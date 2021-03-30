from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import *
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from .forms import *
from django.contrib import messages
from datetime import date

from django.forms import inlineformset_factory


def Homepage(request):
    ro = room_search()
    fo = faculty_search()
    co = course_search()
    return render(request, 'Homepage.html', context={'ro': ro, 'fo': fo, 'co': co})


def search_room_wise(request):
    if request.method == "POST":
        ro = room_search(request.POST)
        print(ro.errors)
        if ro.is_valid():
            room = request.POST['room']
            rm = room_no.objects.get(id=room)
            matrix = [[' ' for i in range(10)] for j in range(len(DAYS_CHOICES))]
            for k, l in enumerate(DAYS_CHOICES):
                t = 0
                for j in range(10):
                    if j == 0:
                        matrix[k][0] = l[0]
                    else:
                        try:
                            matrix[k][j] = table2.objects.get(
                                room1=room,
                                choose__academic_year1__show=True,
                                choose__sem1__show1=True, day=l[0],
                                time=TIME_CHOICES[t][0])
                        except table2.DoesNotExist:
                            pass
                        t = t + 1
            tg = TIME_CHOICES
            return render(request, 'Room-Wise_Timetable.html', context={'matrix': matrix, 'rm': rm, 'tg': tg})
        else:
            messages.error(request, "Not uploaded Yet")
            ro = room_search()
            return render(request, 'Room-Wise_Search.html', context={'ro': ro})
    else:
        ro = room_search()
        return render(request, 'Room-Wise_Search.html', context={'ro': ro})


def search_faculty_wise(request):
    if request.method == "POST":
        fo = faculty_search(request.POST)
        print(fo.errors)
        if fo.is_valid():
            fac = request.POST['faculty']
            fc = faculty.objects.get(id=fac)
            matrix = [[' ' for i in range(10)] for j in range(len(DAYS_CHOICES))]
            for k, l in enumerate(DAYS_CHOICES):
                t = 0

                for j in range(10):
                    if j == 0:
                        matrix[k][0] = l[0]

                    else:
                        try:
                            matrix[k][j] = table2.objects.get(
                                Q(faculty_name1=fac) | Q(faculty_name2=fac), choose__academic_year1__show=True,
                                choose__sem1__show1=True, day=l[0],
                                time=TIME_CHOICES[t][0])
                        except table2.DoesNotExist:

                            pass
                        t = t + 1
            tg = TIME_CHOICES
            return render(request, 'Faculty-Wise_Timetable.html', context={'matrix': matrix, 'fc': fc, 'tg': tg})

        else:
            messages.error(request, "Not uploaded Yet")
            fo = faculty_search()
            return render(request, 'Faculty-Wise_Search.html', context={'fo': fo})

    else:
        fo = faculty_search()
        return render(request, 'Faculty-Wise_Search.html', context={'fo': fo})


def search_course_wise(request):
    if request.method == "POST":
        co = course_search(request.POST)
        print(co.errors)
        if co.is_valid():
            cn = request.POST['CourseName']
            sm = request.POST['Sem']
            cv = Course.objects.get(id=cn)
            sm = sem.objects.get(id=sm)
            matrix = [[' ' for i in range(10)] for j in range(len(DAYS_CHOICES))]
            for k, l in enumerate(DAYS_CHOICES):
                t = 0
                for j in range(10):
                    if j == 0:
                        matrix[k][0] = l[0]

                    else:
                        try:
                            matrix[k][j] = table2.objects.filter(choose__course_name=cn, choose__sem1=sm,
                                                                 choose__academic_year1__show=True,
                                                                 day=l[0],
                                                                 time=TIME_CHOICES[t][0])
                        except table2.DoesNotExist:

                            pass
                        t = t + 1
            tg = TIME_CHOICES
            return render(request, 'Course-Wise_Timetable.html',
                          context={'matrix': matrix, 'cv': cv, 'sm': sm, 'tg': tg})

        else:
            messages.error(request, "Not uploaded Yet")
            co = course_search()
            return render(request, 'Course-Wise_Search.html', context={'co': co})

    else:
        co = course_search()
        return render(request, 'Course-Wise_Search.html', context={'co': co})


@login_required(login_url='/Login_User')
def admin_homepage(request):
    if request.method == "POST":
        s1 = search_form1(request.POST)
        if s1.is_valid():
            ac = request.POST['acad_yr']
            cn = request.POST['CourseName']
            cv = Course.objects.get(id=cn)
            sm = request.POST['Sem']
            matrix = [[' ' for i in range(10)] for j in range(len(DAYS_CHOICES))]
            for k, l in enumerate(DAYS_CHOICES):
                t = 0
                for j in range(10):
                    if j == 0:
                        matrix[k][0] = l[0]
                    else:
                        try:
                            matrix[k][j] = table2.objects.filter(choose__course_name=cn, choose__academic_year1=ac,
                                                                 choose__sem1=sm,
                                                                 day=l[0], time=TIME_CHOICES[t][0])

                        except table2.DoesNotExist:
                            pass
                        t = t + 1
            tg = TIME_CHOICES
            s = sem.objects.all()
            a = year.objects.all()
            messages.success(request, "Searched Results:")
            return render(request, 'Search_Timetable.html',
                          context={'matrix': matrix, 'cv': cv, 'tg': tg, 'sm': sm, 'ac': ac, 's': s, 'a': a})
        else:
            messages.error(request, "Not Found anything")
            s1 = search_form1()
            s = sem.objects.all()
            a = year.objects.all()
            return render(request, 'Admin-Panel.html', context={'s1': s1, 's': s, 'a': a})
    else:
        s1 = search_form1()
        s = sem.objects.all()
        a = year.objects.all()
        return render(request, 'Admin-Panel.html', context={'s1': s1, 's': s, 'a': a})


@login_required(login_url='/Login_User')
def check_old(request):
    if request.method == "POST":
        sfrm = findlast_form(request.POST)
        if sfrm.is_valid():
            a = request.POST['Year']
            b = request.POST['faculty']
            c = request.POST['Sem']
            bi = faculty.objects.get(id=b)
            ai = year.objects.get(id=a)
            matrix = [[' ' for i in range(10)] for j in range(len(DAYS_CHOICES))]
            for k, l in enumerate(DAYS_CHOICES):
                t = 0
                for j in range(10):
                    if j == 0:
                        matrix[k][0] = l[0]
                    else:
                        try:
                            if c == TICK_CHOICES[0][0]:
                                matrix[k][j] = table2.objects.get(Q(faculty_name1=b) | Q(faculty_name2=b),
                                                                  choose__academic_year1=a, choose__sem1__show1=True,
                                                                  day=l[0], time=TIME_CHOICES[t][0])
                            else:
                                matrix[k][j] = table2.objects.get(Q(faculty_name1=b) | Q(faculty_name2=b),
                                                                  choose__academic_year1=a, choose__sem1__show1=False,
                                                                  day=l[0], time=TIME_CHOICES[t][0])
                        except table2.DoesNotExist:
                            pass
                        t = t + 1
            tg = TIME_CHOICES
            s = sem.objects.all()

            a = year.objects.all()
            return render(request, 'old_faculty_Timetable.html',
                          context={'matrix': matrix, 'bi': bi, 'tg': tg, 'ai': ai, 's': s, 'a': a})
        else:
            messages.error(request, "Not Found anything")
            sfrm = findlast_form()
            s = sem.objects.all()

            a = year.objects.all()
            return render(request, 'Search_old_faculty_timetable.html', context={'sfrm': sfrm, 's': s, 'a': a})

    else:
        sfrm = findlast_form()
        s = sem.objects.all()

        a = year.objects.all()
        return render(request, 'Search_old_faculty_timetable.html', context={'sfrm': sfrm, 's': s, 'a': a})


@login_required(login_url='/Login_User')
def faculty_create(request):
    if request.method == "POST":
        facfrm = facul_form(request.POST)
        if facfrm.is_valid():
            facfrm.save()
            f = faculty.objects.all()
            facfrm = facul_form()
            s = sem.objects.all()
            a = year.objects.all()
            messages.success(request, "Created Successfully")
            return render(request, "faculty.html", context={'facfrm': facfrm, 'f': f, 's': s, 'a': a})
        else:
            messages.error(request, "Please enter the data correctly")
            facfrm = facul_form()
            f = faculty.objects.all()
            s = sem.objects.all()
            a = year.objects.all()
            return render(request, "faculty.html", context={'facfrm': facfrm, 'f': f, 's': s, 'a': a})


    else:
        facfrm = facul_form()
        f = faculty.objects.all()
        s = sem.objects.all()
        a = year.objects.all()
        return render(request, "faculty.html", context={'facfrm': facfrm, 'f': f, 's': s, 'a': a})


@login_required(login_url='/Login_User')
def faculty_update(request, id):
    fc = faculty.objects.get(id=id)
    if request.method == "POST":
        facfrm = facul_form(request.POST, instance=fc)
        if facfrm.is_valid():
            facfrm.save()
            f = faculty.objects.all()
            facfrm = facul_form()
            s = sem.objects.all()
            a = year.objects.all()
            messages.success(request, "Successfully Updated")
            return render(request, "faculty.html", context={'facfrm': facfrm, 'f': f, 's': s, 'a': a})
        else:
            messages.error(request, "Please enter the data correctly")
            f = faculty.objects.all()
            s = sem.objects.all()
            a = year.objects.all()
            facfrm = facul_form(instance=fc)
            return render(request, "faculty.html", context={'facfrm': facfrm, 'f': f, 'a': a, 's': s})

    else:
        f = faculty.objects.all()
        s = sem.objects.all()
        a = year.objects.all()
        facfrm = facul_form(instance=fc)
        return render(request, "faculty.html", context={'facfrm': facfrm, 'f': f, 'a': a, 's': s})


@login_required(login_url='/Login_User')
def fac_del(request, id):
    fc = faculty.objects.get(id=id)
    fc.delete()
    f = faculty.objects.all()
    facfrm = facul_form()
    s = sem.objects.all()
    a = year.objects.all()
    messages.success(request, "Successfully Deleted")
    return render(request, "faculty.html", context={'facfrm': facfrm, 'f': f, 'a': a, 's': s})


@login_required(login_url='/Login_User')
def create_acad(request):
    if request.method == "POST":
        acdfrm = acad_form(request.POST)
        if acdfrm.is_valid():
            acdfrm.save()
            a = year.objects.all()
            acdfrm = acad_form()
            s = sem.objects.all()
            s1 = search_form1()
            messages.success(request, "Successfully Created")
            return render(request, 'Admin-Panel.html', context={'a': a, 's': s, 's1': s1})
        else:
            messages.error(request, "Please enter the data correctly")
            a = year.objects.all()
            acdfrm = acad_form()
            s = sem.objects.all()

            return render(request, 'Academic_Year.html', context={'a': a, 'acdfrm': acdfrm, 's': s})

    else:
        a = year.objects.all()
        acdfrm = acad_form()
        s = sem.objects.all()

        return render(request, 'Academic_Year.html', context={'a': a, 'acdfrm': acdfrm, 's': s})


@login_required(login_url='/Login_User')
def update_acad(request, id):
    ac = year.objects.get(id=id)
    if request.method == "POST":
        acdfrm = acad_form(request.POST, instance=ac)
        if acdfrm.is_valid():
            acdfrm.save()
            a = year.objects.all()
            acdfrm = acad_form()
            s = sem.objects.all()
            s1 = search_form1()
            messages.success(request, "Successfully Updated")
            return render(request, 'Admin-Panel.html', context={'a': a, 's': s, 's1': s1})
        else:
            messages.error(request, "Please enter the data correctly")
            a = year.objects.all()
            s = sem.objects.all()

            acdfrm = acad_form(instance=ac)
            return render(request, 'Academic_Year.html', context={'a': a, 's': s, 'acdfrm': acdfrm})

    else:
        a = year.objects.all()
        s = sem.objects.all()

        acdfrm = acad_form(instance=ac)
        return render(request, 'Academic_Year.html', context={'a': a, 's': s, 'acdfrm': acdfrm})


@login_required(login_url='/Login_User')
def delete_acd(request, id):
    a = year.objects.get(id=id)
    a.delete()
    ac = year.objects.all()
    acdfrm = acad_form()
    a = year.objects.all()
    s = sem.objects.all()
    s1 = search_form1()
    messages.success(request, "Successfully Deleted")
    return render(request, 'Admin-Panel.html', context={'a': a, 's': s, 's1': s1})


@login_required(login_url='/Login_User')
def update_sem(request, id):
    se = sem.objects.get(id=id)
    if request.method == "POST":
        sfrm = sem_form(request.POST, instance=se)
        if sfrm.is_valid():
            sfrm.save()
            s = sem.objects.all()
            a = year.objects.all()
            sfrm = sem_form()
            s1 = search_form1()
            messages.success(request, "Successfully Updated")
            return render(request, "Admin-Panel.html", context={'a': a, 's': s, 's1': s1})
        else:
            messages.error(request, "Please enter the data correctly")
            s = sem.objects.all()
            sfrm = sem_form(instance=se)

            a = year.objects.all()
            return render(request, "Update_Semester.html", context={'sfrm': sfrm, 's': s, 'a': a})
    else:
        s = sem.objects.all()
        sfrm = sem_form(instance=se)

        a = year.objects.all()
        return render(request, "Update_Semester.html", context={'sfrm': sfrm, 's': s, 'a': a})


@login_required(login_url='/Login_User')
def create_class(request):
    if request.method == "POST":
        tfrm1 = timetable_form1(request.POST)
        if tfrm1.is_valid():
            tfrm1.save()
            tfrm1 = timetable_form1()
            t = table1.objects.all()
            s = sem.objects.all()
            a = year.objects.all()
            messages.success(request, "Successfully Created")
            return render(request, "Class.html", context={'tfrm1': tfrm1, 't': t, 's': s, 'a': a})
        else:
            messages.error(request, "Please enter the data correctly")
            tfrm1 = timetable_form1()
            t = table1.objects.all()
            s = sem.objects.all()
            a = year.objects.all()
            return render(request, "Class.html", context={'tfrm1': tfrm1, 't': t, 's': s, 'a': a})

    else:
        tfrm1 = timetable_form1()
        t = table1.objects.all()
        s = sem.objects.all()
        a = year.objects.all()
        return render(request, "Class.html", context={'tfrm1': tfrm1, 't': t, 's': s, 'a': a})


@login_required(login_url='/Login_User')
def create_timetable2(request, id):
    table2formset = inlineformset_factory(table1, table2, timetable_form2,can_delete=True)

    tble1 = table1.objects.get(id=id)
    tble2 = table2.objects.filter(choose__id=tble1.id)
    print(len(tble2))
    d = len(tble2) + 4
    ll = []
    i = 0
    for j in range(d):
        ll.append(j)
    if request.method == "POST":
        formset = table2formset(request.POST, instance=tble1)
        if formset.is_valid():
            formset.save()
            t = table2.objects.filter(choose__id=id)
            matrix = [[' ' for i in range(10)] for j in range(len(DAYS_CHOICES))]
            for k, l in enumerate(DAYS_CHOICES):
                t = 0
                for j in range(10):
                    if j == 0:
                        matrix[k][0] = l[0]

                    else:
                        try:
                            matrix[k][j] = table2.objects.filter(choose__id=id, day=l[0], time=TIME_CHOICES[t][0])
                        except table2.DoesNotExist:

                            pass
                        t = t + 1
            tg = TIME_CHOICES
            s = sem.objects.all()
            a = year.objects.all()
            messages.success(request, "Successfully Created")
            return render(request, 'Created.html',
                          context={'matrix': matrix, 'tg': tg, 'id': id, 'a': a, 's': s, 'tble1': tble1})
        else:
            print(formset.errors)
            l = formset.errors
            formset = table2formset(instance=tble1)
            request.session['tid'] = tble1.id
            s = sem.objects.all()
            a = year.objects.all()
            return render(request, 'Create_Table.html',
                          context={'formset': formset, 'll': ll, 's': s, 'a': a, 'tble1': tble1, 'l': l})

    else:

        formset = table2formset(instance=tble1)
        request.session['tid'] = tble1.id
        s = sem.objects.all()
        a = year.objects.all()
        return render(request, 'Create_Table.html',
                      context={'formset': formset, 'll': ll, 's': s, 'a': a, 'tble1': tble1})


@login_required(login_url='/Login_User')
def update_class(request, id):
    tb = table1.objects.get(id=id)
    if request.method == "POST":
        tfrm1 = timetable_form1(request.POST, instance=tb)
        if tfrm1.is_valid():
            tfrm1.save()
            t = table1.objects.all()
            tfrm1 = timetable_form1()
            s = sem.objects.all()
            a = year.objects.all()
            messages.success(request, "Successfully Updated")
            return render(request, "Class.html", context={'t': t, 'tfrm1': tfrm1, 's': s, 'a': a})
        else:
            messages.error(request, "Please enter the data correctly")
            t = table1.objects.all()
            tfrm1 = timetable_form1(instance=tb)
            s = sem.objects.all()
            a = year.objects.all()
            return render(request, "Class.html", context={'t': t, 'tfrm1': tfrm1, 's': s, 'a': a})


    else:
        t = table1.objects.all()
        tfrm1 = timetable_form1(instance=tb)
        s = sem.objects.all()
        a = year.objects.all()
        return render(request, "Class.html", context={'t': t, 'tfrm1': tfrm1, 's': s, 'a': a})


@login_required(login_url='/Login_User')
def update_table2(request, id):
    tc = table2.objects.get(id=id)
    if request.method == "POST":
        tfrm2 = timetable_form2(request.POST, instance=tc)
        if tfrm2.is_valid():
            tfrm2.save()
            s1 = search_form1()
            s = sem.objects.all()
            a = year.objects.all()
            messages.success(request, "Successfully Updated")
            return render(request, 'Admin-Panel.html', context={'s1': s1, 's': s, 'a': a})

        else:
            messages.error(request, "Please enter the data correctly")
            tfrm2 = timetable_form2(instance=tc)
            s = sem.objects.all()
            a = year.objects.all()
            return render(request, 'Update_Timetable.html', context={'tfrm2': tfrm2, 's': s, 'a': a})

    else:
        tfrm2 = timetable_form2(instance=tc)
        s = sem.objects.all()
        a = year.objects.all()
        return render(request, 'Update_Timetable.html', context={'tfrm2': tfrm2, 's': s, 'a': a})


@login_required(login_url='/Login_User')
def del_class(request, id):
    ta = table1.objects.get(id=id)
    tb = table2.objects.filter(choose__id=id)
    ta.delete()
    for j in tb:
        j.delete()
    t = table1.objects.all()
    tfrm1 = timetable_form1()
    s = sem.objects.all()
    a = year.objects.all()
    messages.success(request, "Successfully Deleted")
    return render(request, "Class.html", context={'t': t, 'tfrm1': tfrm1, 's': s, 'a': a})


@login_required(login_url='/Login_User')
def del_table2(request, id):
    tc = table2.objects.get(id=id)
    tc.delete()
    s1 = search_form1()
    s = sem.objects.all()
    a = year.objects.all()
    messages.success(request, "Successfully Deleted")
    return render(request, 'Admin-Panel.html', context={'s1': s1, 's': s, 'a': a})


def load_sem(request):
    dd = request.GET.get('day')
    ti = request.GET.get('time')

    try:
        ds = table1.objects.get(id=request.session['tid'])
        print("table1", ds)
        print(ds.academic_year1)
        print("date", dd)
        print("time", ti)
        ac = table2.objects.filter(choose__academic_year1=ds.academic_year1, choose__sem1__show1=True, day=dd, time=ti)
        print("table2", ac)
        lw = []
        for j in ac:
            lw.append(j.room1)

        print("room", lw)

        zx = room_no.objects.exclude(room__in=lw)
        print("room2", zx)

    except:
        zx = room_no.objects.all()

    return render(request, 'room_dropdown_list_options.html', {'zx': zx})


def log(request):
    if request.user.is_authenticated:
        s1 = search_form1()
        s = sem.objects.all()
        a = year.objects.all()
        return render(request, 'Admin-Panel.html', context={'s1': s1, 's': s, 'a': a})
    else:
        if request.method == 'POST':
            frm = login_form(request.POST)
            username = request.POST.get('Username')
            password = request.POST.get('Password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                s1 = search_form1()
                s = sem.objects.all()
                a = year.objects.all()
                print(frm.errors)
                messages.success(request, "Successfully Logged in")
                return render(request, 'Admin-Panel.html', context={'s1': s1, 's': s, 'a': a})
            else:
                print(frm.errors)
                frm = login_form()
                context = {'frm': frm}
                return render(request, 'User_Login.html', context)
        else:

            frm = login_form()
            context = {'frm': frm}
            return render(request, 'User_Login.html', context)


@login_required(login_url='/Login_User')
def logout_user(request):
    logout(request)
    frm = login_form()
    context = {'frm': frm}
    messages.success(request, "Successfully Logged out")
    return render(request, 'User_Login.html', context)
