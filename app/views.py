from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import logout,authenticate,login
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from app.models import *
from django.core.paginator import Paginator

import requests
from bs4 import BeautifulSoup
import re


user_permissions = [

'Can add session',
'Can change session',
'Can delete session',
'Can add actions',
'Can change actions',
'Can delete actions',
'Can add check lists',
'Can change check lists',
'Can delete check lists',
]




def error_page(request,err):
    return render(request,'error.html',context={"err":err})


def home(request):
    #url = "https://ru.dotabuff.com/heroes/winning"
    #r = requests.get(url, headers = {"user-agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64)"})
    #html = r.text
    #soup = BeautifulSoup(html, 'html.parser')
    #text_filter_1 = soup.get_text().split("УСП")[1]
    #text_filter_2 = text_filter_1.split("Обновлено")[0].replace(" ", "")
    #text_filter_3 = re.findall("[a-zA-Z]+", text_filter_2)
    #top_30_heroes = text_filter_3[0:31]

    #hero_stats = re.split("[a-zA-Z]+", text_filter_2)[1:31]
    #allz = [x + " " + y for x, y in zip(top_30_heroes, hero_stats)]

    top_30_heroes = "xxx"
    return render(request, 'home.html',{'topheroes':top_30_heroes} #, 'topstats':hero_stats, 'ttt':allz})



def about(request):
    return render(request,'about.html')

def login_user(request):
    if request.method == 'GET':
        return render(request,'login.html')

    elif request.method == 'POST':
        user = authenticate(username=request.POST['user_login'], password=request.POST['user_password'])
        if user:
            login(request, user)
            return listofcases(request)
        else:
            return error_page(request,"invalid password or login")
    else:
        return error_page(request,"invalid method")

def logout_user(request):
    logout(request)
    return render(request,'after_logout.html',{'username':request.user.username})

def register(request):
    if request.method == 'GET':
        return render(request,'register.html')

    elif request.method == 'POST' and not request.user.is_authenticated:
        _login = request.POST['user_login']
        email = request.POST['user_email']
        password = request.POST['user_password']
        password_retype = request.POST['user_password_retype']
        if password != password_retype:
            return error_page(request,'recheck passwords')

        #TODO: validate post data
        user = User(username=_login,first_name=_login,email=email,password=password)
        user.set_password(password) # without hash algorithm (raw)
        if not user:
            return error_page(request,'invalid data')

        user.save()

        for perm in user_permissions:
            user.user_permissions.add(Permission.objects.get(name=perm))
        user.save()
        
        login(request,user)
        authenticate(request,username=_login,password=password)
        return HttpResponseRedirect('/listofcases/')
    
def createchecklist(request):
    
    if request.method == 'POST':
        author = User.objects.get(username=request.user)
        actions = request.POST.getlist('action')
        proj_name = request.POST['project_name']
        checklist_name = request.POST['checklist_name']
        print(request.POST)


        #

        checklist = CheckLists.objects.create( name=checklist_name,project_name=proj_name,author=author )
        checklist.save()

        #

        for a in actions:
            action = Actions.objects.create(name=checklist_name,project=checklist,notes=a)
            action.save()

        #

        return HttpResponseRedirect('/listofcases/')
    elif request.method == 'GET':
        return render(request,'createchecklist.html')

def listofcases(request):
    cases_by_user_active = CheckLists.objects.filter(is_active=True,is_visible=True)
    cases_by_user_complete = CheckLists.objects.filter(is_active=False,is_visible=True)

    return render(request,'listofcases.html',{"cases_active":cases_by_user_active,"cases_complete":cases_by_user_complete})


def checklist(request,id):

    checklist = CheckLists.objects.get(pk=id)
    actions = Actions.objects.filter(project=checklist)
    return render(request,'checklist.html',{'checklist':checklist,'actions':actions})
    # if checklist.author == request.user:
    #     return render(request,'checklist.html',{'checklist':checklist,'actions':actions})
    # else:
    #     return error_page(request,'invalid checklist')

def toggle_status(request,id):
    c = CheckLists.objects.get(pk = id)
    if c.is_active:
        c.is_active = False
    else:
        c.is_active = True
    c.save()

    return listofcases(request)


def toggle_action(request,action_id,checklist_id):
    a = Actions.objects.get(pk=action_id)

    if a.status == False:
        a.status = True
    else:
        a.status = False

    c = CheckLists.objects.get(pk=checklist_id)
    c.touched = True
    c.save()
    a.save()
    return HttpResponseRedirect('/checklist/{}'.format(checklist_id))

def finish_checklist(request,checklist_id):
    c = CheckLists.objects.get(pk = checklist_id)
    c.is_active = False
    c.save()
    return listofcases(request)
