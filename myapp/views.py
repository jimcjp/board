from django.shortcuts import render,redirect
from myapp.models import student
from django import forms
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


@login_required
def listall(request):
    try:
        unit = student.objects.all().order_by('id')
    except:
        errormessage = "讀取錯誤"

    return render(request,"listall.html",locals())



def index(request):
    try:
        unit = student.objects.all().order_by('id')
    except:
        errormessage = "讀取錯誤"
    if request.session.get("is_login") == True:
        #name = request.session.get("user", None)
        return redirect('/listall/')
    '''else:
        return redirect('/listall/')'''
    return render(request,"index.html",locals())



class register(forms.Form):
    name = forms.CharField(max_length=20, required=True)
    sex = forms.CharField(max_length=2, required=True)
    birthday = forms.DateField(required=True)
    email = forms.EmailField(max_length=100, required=True)
    phone = forms.CharField(max_length=50, required=True)
    addr = forms.CharField(max_length=255, required=True)


@login_required
def addstudent(request):
    if request.method =="POST":#如果是以post方式才處理
        tsai = register(request.POST)
        #print(tsai.changed_data)
        if tsai.is_valid():
            inname = tsai.cleaned_data['name']
            insex = tsai.cleaned_data['sex']
            inbirthday = tsai.cleaned_data['birthday']
            inemail = tsai.cleaned_data['email']
            inphone = tsai.cleaned_data['phone']
            inaddr = tsai.cleaned_data['addr']
            unit = student.objects.create(cName=inname, cSex=insex, cBirthday=inbirthday,
                                          cEmail=inemail, cPhone=inphone, cAdd=inaddr)
            unit.save()
            message = '已新增'
            #print(unit)
            return redirect('/listall/')
        else:
            message = '驗證失敗'
    else:
        #message = '新增失敗'
        tsai = register()
    return render(request,"addstudent.html",locals())



@login_required
def delstudent(request):
    if request.method == 'POST':
        cc = request.POST['id']
    try:
        unit = student.objects.get(id = cc)
        unit.delete()
        return redirect('/index/')
    except:
        message = '讀取錯誤'
    return render(request, 'delstudent.html',locals())


@login_required
def editstudent(request,id,mode):
        if mode == "load":
            unit = student.objects.get(id=id)
            strdate = str(unit.cBirthday)
            strdate2 = strdate.replace('年','-')
            strdate2 = strdate.replace('月','-')
            strdate2 = strdate.replace('日','-')
            unit.cBirthday = strdate2
            return render(request, 'editstudent.html', locals())
        elif mode == "save":
            unit = student.objects.get(id=id)
            unit.cName =request.POST['name']
            unit.cSex =request.POST['sex']
            unit.cBirthday =request.POST['birthday']
            unit.cEmail =request.POST['email']
            unit.cPhone =request.POST['phone']
            unit.cAdd =request.POST['add']
            unit.save()  #寫入資料庫
            #message = '已修改....'
            return redirect('/listall/')




def login(request):
    if request.method == 'POST':
        name = request.POST['username']
        pw = request.POST['password']
        user = auth.authenticate(username=name , password=pw)
        if user is not None:
            if user.is_active:
                auth.login(request,user)
                msg = '登入成功'
                request.session["is_login"] = True  # 在session中增加键值对
                request.session["user"] = name
                return redirect('/listall/')
                #return render(request, 'listall.html', locals())
            else:
                msg = '帳號尚未啟用'
        else:
            msg = '登入失敗'
    return render(request,'login.html',locals())



def logout(request):
    auth.logout(request)
    request.session.clear()
    '''request.cookies.clear()'''
    return redirect('/index/')



class addmem(forms.Form):
    name = forms.CharField(max_length=20, required=True)
    pw = forms.CharField(widget=forms.PasswordInput, required=True)
    email = forms.EmailField(max_length=100, required=True)




def adduser(request):
    if request.method =="POST":#如果是以post方式才處理
        mem = addmem(request.POST)
        if mem.is_valid():  #如果没有填，form.is_valid()就会返回false
            inname = mem.cleaned_data['name']
            inpw = mem.cleaned_data['pw']
            inemail = mem.cleaned_data['email']
            unit = User.objects.create_user(username=inname,password=inpw,email=inemail)
            unit.is_staff=True #工作人員狀態
            unit.save()
            return redirect('/index/')
    else:
        mem = addmem()
    return render(request,'adduser.html',locals())
# Create your views here.
