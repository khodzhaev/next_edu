from django.shortcuts import render, redirect, HttpResponse, Http404
from .models import Group, Student, Homework, Lesson, Test, TestStudent, TestItem
from pages.models import Clients
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.db.models import Count
from django.contrib.auth.models import User
from django.contrib.auth.hashers import PBKDF2PasswordHasher
from django.contrib.auth.decorators import login_required
import os
from django.conf import settings


def lastname_admin_check(user):
    return user.last_name == 'Администратор'


@login_required(login_url='index')
@user_passes_test(lastname_admin_check)
def panel(requests):
    groups = Group.objects.all()
    students = Student.objects.all()
    context = {
        'groups': groups.count(),
        'students': students.count()
    }
    return render(requests, 'panel/panel.html', context)


##########################################################################
# Groups
##########################################################################
@login_required(login_url='index')
@user_passes_test(lastname_admin_check)
def groups(requests):
    groups = Group.objects.all()
    context = {
        'groups': groups
    }
    return render(requests, 'panel/groups.html', context)


@login_required(login_url='index')
@user_passes_test(lastname_admin_check)
def groups_add(requests):
    if requests.method == 'POST':
        Group.objects.create(
            title=requests.POST['title'],
            level=requests.POST['level'],
        )
        return redirect('groups')
    return redirect('groups')


@login_required(login_url='index')
@user_passes_test(lastname_admin_check)
def groups_edit(requests, id):
    if requests.method == 'POST':
        g = Group.objects.get(id=id)
        g.title = requests.POST['title']
        g.level = requests.POST['level']
        g.completed = requests.POST['completed']
        g.save()
        return redirect('groups')
    return redirect('groups')


@login_required(login_url='index')
@user_passes_test(lastname_admin_check)
def groups_delete(requests, id):
    if requests.method == 'POST':
        g = Group.objects.get(id=id)
        g.delete()
        return redirect('groups')
    return redirect('groups')


##########################################################################
# Students
##########################################################################
@login_required(login_url='index')
@user_passes_test(lastname_admin_check)
def students(requests):
    students = Student.objects.all()
    groups = Group.objects.all()
    context = {
        'students': students,
        'groups': groups,
    }
    return render(requests, 'panel/students.html', context)


@login_required(login_url='index')
@user_passes_test(lastname_admin_check)
def students_add(requests):
    if requests.method == 'POST':
        u = User.objects.create_user(
            username=requests.POST['username'],
            password=requests.POST['password'],
        )
        group = requests.POST['group']
        s = Student.objects.get(user_id=User.objects.get(id=u.id))
        s.group = Group.objects.get(title=group)
        s.fname = requests.POST['first_name']
        s.rating = 100
        s.save()
        return redirect('students')
    return redirect('students')


@login_required(login_url='index')
@user_passes_test(lastname_admin_check)
def students_edit(requests, id):
    if requests.method == 'POST':
        u = User.objects.get(id=id)
        s = Student.objects.get(user=u)
        s.fname = requests.POST['first_name']
        s.rating = requests.POST['rating']
        s.group = Group.objects.get(title=requests.POST['group'])
        u.username = requests.POST['username']
        s.save()
        u.save()
        return redirect('students')
    return redirect('students')


@login_required(login_url='index')
@user_passes_test(lastname_admin_check)
def students_edit_password(requests, id):
    if requests.method == 'POST':
        u = User.objects.get(id=id)
        password = requests.POST['password']
        hasher = PBKDF2PasswordHasher()
        password = hasher.encode(password=password, salt='salt', iterations=50000)
        u.password = password
        u.save()
        return redirect('students')
    return redirect('students')


@login_required(login_url='index')
@user_passes_test(lastname_admin_check)
def students_delete(requests):
    if requests.method == 'POST':
        u = User.objects.get(username=requests.POST['login'])
        u.delete()
        return redirect('students')
    return redirect('students')


##########################################################################
# Lessons
##########################################################################
@login_required(login_url='index')
@user_passes_test(lastname_admin_check)
def lessons(requests):
    lessons = Lesson.objects.all()
    groups = Group.objects.all()
    context = {
        'lessons': lessons,
        'groups': groups,
    }
    return render(requests, 'panel/lessons.html', context)


@login_required(login_url='index')
@user_passes_test(lastname_admin_check)
def lessons_add(requests):
    if requests.method == 'POST' and requests.FILES['file']:
        Lesson.objects.create(
            title=requests.POST['title'],
            group=Group.objects.get(title=requests.POST['group']),
            video=requests.POST['video'],
            lesson=requests.FILES['file'],
        )
        return redirect('lessons')
    return redirect('lessons')


@login_required(login_url='index')
@user_passes_test(lastname_admin_check)
def lessons_edit(requests, id):
    if requests.method == 'POST' or requests.FILES['file']:
        l = Lesson.objects.get(id=id)
        l.title = requests.POST['title']
        l.group = Group.objects.get(id=requests.POST['group'])
        l.video = requests.POST['video']

        try:
            expath = l.lesson.path
            l.lesson = requests.FILES['file']
            os.remove(expath)
        except:
            pass

        l.save()
        return redirect('lessons')
    return redirect('lessons')


@login_required(login_url='index')
@user_passes_test(lastname_admin_check)
def lessons_delete(requests, id):
    if requests.method == 'POST':
        l = Lesson.objects.get(id=id)
        os.system('rm {}'.format(l.lesson.path))
        l.delete()
        return redirect('lessons')
    return redirect('lessons')


##########################################################################
# Clients
##########################################################################
@login_required(login_url='index')
@user_passes_test(lastname_admin_check)
def clients(requests):
    clients = Clients.objects.all()
    context = {
        'clients': clients,
    }
    return render(requests, 'panel/clients.html', context)


@login_required(login_url='index')
@user_passes_test(lastname_admin_check)
def clients_complete(requests, id):
    c = Clients.objects.get(id=id)
    if c.processed == True:
        c.processed = False
    elif c.processed == False:
        c.processed = True
    c.save()
    return redirect('clients')


##########################################################################
# HWs
##########################################################################
@login_required(login_url='index')
@user_passes_test(lastname_admin_check)
def hws(requests):
    hws = Homework.objects.all()
    groups = Group.objects.all()
    context = {
        'hws': hws,
        'groups': groups,
    }
    return render(requests, 'panel/hws.html', context)


@login_required(login_url='index')
@user_passes_test(lastname_admin_check)
def hws_delete(requests, id):
    if requests.method == 'POST':
        h = Homework.objects.get(id=id)
        os.system('rm {}'.format(h.upload.path))
        h.delete()
        return redirect('hws')
    return redirect('hws')


@login_required(login_url='index')
@user_passes_test(lastname_admin_check)
def hws_complete(requests, id):
    h = Homework.objects.get(id=id)
    if h.processed == True:
        h.processed = False
    elif h.processed == False:
        h.processed = True
    h.save()
    return redirect('hws')


##########################################################################
# Download function
##########################################################################


def download(requests, id):
    file_lesson = Lesson.objects.get(id=id)
    file_path = os.path.join(settings.MEDIA_ROOT, file_lesson.lesson.path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/zip")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404


def download_hws(requests, id):
    file_lesson = Homework.objects.get(id=id)
    file_path = os.path.join(settings.MEDIA_ROOT, file_lesson.upload.path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/zip")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404
