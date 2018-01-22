# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from models import *
from datetime import datetime
import bcrypt
from django.contrib import messages
from django.shortcuts import render, redirect

def index(request):
    context = {
        'users':User.objects.all()
    }
    return render(request, 'users/signin.html', context)

def edit(request, number):
    context = {
        'user':User.objects.get(id=number),
        'curr_user':User.objects.get(id=request.session['curr_user_id'])
    }
    return render(request, 'users/editUser.html', context)

def success(request):
    if request.session['curr_user_id'] != 'none':
        return redirect('dashboard/success/')
    
    return redirect('/signin')

def register(request):
    request.session['curr_user_id'] = 'none'
    return render(request, 'users/register.html')

def registerUser(request):
    if request.method == "POST":
        fName = request.POST['fName']
        lName = request.POST['lName']
        email = request.POST['email']
        birthday = request.POST['birthday']
        password = request.POST['password']
        pw_conf = request.POST['pw_conf']

        errors = User.objects.validate(request.POST)
        if len(errors) > 0:
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/register/')
        else:
            User.objects.create(fName=fName, lName=lName, email=email, birthday=birthday, password=bcrypt.hashpw(password.encode(), bcrypt.gensalt()))
            if User.objects.count() == 1:
                user = User.objects.last()
                user.level = 'admin'
            else:
                user = User.objects.last()
                user.level = 'normal'
                user.save()
            messages.add_message(request, messages.INFO, 'Success. Now log in.')
            return redirect('/signin/')

def updateInfo(request):
    if request.method == "POST":
        if 'fName' in request.POST:
            updateData = {
                'fName':request.POST['fName'],
                'lName':request.POST['lName'],
                'email':request.POST['email'],
                'birthday':request.POST['birthday'],
            }
            errors = User.objects.validateInfo(request.POST)
            if len(errors) > 0:
                for tag, error in errors.iteritems():
                    messages.error(request, error, extra_tags=tag)
                return redirect('/users/' + str(request.session['curr_user_id']) + '/edit')
            else:
                user = User.objects.get(id=request.session['curr_user_id'])
                user.fName = updateData['fName']
                user.lName = updateData['lName']
                user.email = updateData['email']
                user.birthday = updateData['birthday']
                user.save()
                messages.add_message(request, messages.INFO, 'Info successfully updated')
                return redirect('/dashboard/show/' + str(request.session['curr_user_id']))

        elif 'password' in request.POST:
            updateData = {
                'password':request.POST['password'],
                'pw_conf':request.POST['pw_conf'],
            }
            errors = User.objects.validatePW(request.POST)
            if len(errors) > 0:
                for tag, error in errors.iteritems():
                    messages.error(request, error, extra_tags=tag)
                return redirect('/users/' + str(request.session['curr_user_id']) + '/edit')
            else:
                user = User.objects.get(id=request.session['curr_user_id'])
                user.password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
                user.save()
                messages.add_message(request, messages.INFO, 'Password successfully changed')
                return redirect('/dashboard/show/' + str(request.session['curr_user_id']))

        else:
            updateData = {
                'desc':request.POST['desc']
            }
            user.desc = updateData['desc']
            user.save()
            messages.add_message(request, messages.INFO, 'Description successfully updated')
            return redirect('/dashboard/show/' + str(request.session['curr_user_id']))

def signin(request):
    request.session['curr_user_id'] = 'none'
    context = {
        'users':User.objects.all()
    }
    return render(request, 'users/signin.html', context)

def login(request):
    request.session['curr_user_id'] = 'none'
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        
        try:
            user = User.objects.get(email=email)
        except:
            messages.add_message(request, messages.INFO, 'Email does not exist. you suck.')
            return redirect('/signin')

        if bcrypt.checkpw(password.encode(), user.password.encode()):
            request.session['curr_user_id'] = user.id
            return redirect('/success')

        messages.add_message(request, messages.INFO, 'wrong password numbskull.')
        return redirect('/signin')

def logout(request):
    request.session['curr_user_id'] = 'none'
    return redirect('/signin')

def adminEdit(request, number):
    context = {
        'user':User.objects.get(id=number),
        'curr_user':User.objects.get(id=request.session['curr_user_id'])
    }
    return render(request, 'users/adminEditUser.html', context)

def adminUpdateInfo(request):
    if request.method == "POST":
        if 'fName' in request.POST:
            updateData = {
                'id':request.POST['id'],
                'fName':request.POST['fName'],
                'lName':request.POST['lName'],
                'email':request.POST['email'],
                'birthday':request.POST['birthday'],
            }
            errors = User.objects.validateInfo(request.POST)
            if len(errors) > 0:
                for tag, error in errors.iteritems():
                    messages.error(request, error, extra_tags=tag)
                return redirect('/users/adminEdit/' + str(updateData['id']))
            else:
                user = User.objects.get(id=updateData['id'])
                user.fName = updateData['fName']
                user.lName = updateData['lName']
                user.email = updateData['email']
                user.birthday = updateData['birthday']
                user.save()
                messages.add_message(request, messages.INFO, (updateData['fName'] + "'s Info successfully updated"))
                return redirect('/users/adminEdit/' + str(updateData['curr_user_id']))

        elif 'password' in request.POST:
            updateData = {
                'id':request.POST['id'],
                'password':request.POST['password'],
                'pw_conf':request.POST['pw_conf'],
            }
            user = User.objects.get(id=updateData['id'])
            errors = User.objects.validatePW(request.POST)
            if len(errors) > 0:
                for tag, error in errors.iteritems():
                    messages.error(request, error, extra_tags=tag)
                return redirect('/users/adminEdit/' + str(updateData['id']) + '/edit')
            else:
                user = User.objects.get(id=updateData['id'])
                user.password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
                user.save()
                messages.add_message(request, messages.INFO, (User.objects.get(id=updateData['id']).fName + "'s Password successfully changed"))

                return redirect('/users/adminEdit/' + str(updateData['id']))

        else:
            updateData = {
                'id':request.POST['id'],
                'desc':request.POST['desc']
            }
            user = User.objects.get(id=updateData['id'])
            user.desc = updateData['desc']
            user.save()
            messages.add_message(request, messages.INFO, (User.objects.get(id=updateData['id']).fName + "'s Description successfully updated"))
            return redirect('/users/adminEdit/' + str(updateData['id']))

def adminDelete(request, number):
    user = User.objects.get(id=number)
    user.delete()
    return redirect('/dashboard/all')

def updateLevel(request):
    if request.method == 'POST':
        user = User.objects.get(id=request.POST['id'])
        user.level = request.POST['level']
        user.save()
        messages.add_message(request, messages.INFO, (user.fName + "'s user level successfully updated"))
    
    return redirect('/users/adminEdit/' + str(user.id))