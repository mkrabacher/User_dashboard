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
        print 'errors: ', errors
        if len(errors) > 0:
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/register/')
        else:
            User.objects.create(fName=fName, lName=lName, email=email,birthday=birthday, password=bcrypt.hashpw(password.encode(), bcrypt.gensalt()))
            messages.add_message(request, messages.INFO, 'Success. Now log in.')
            return redirect('/signin/')

def updateInfo(request):
    if request.method == "POST":
        updateData = {
            'fName':request.POST['fName'],
            'lName':request.POST['lName'],
            'email':request.POST['email'],
            'birthday':request.POST['birthday'],
            'desc':request.POST['desc'],
        }

        errors = User.objects.validate(request.POST)
        print 'errors: ', errors
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
            user.desc = updateData['desc']
            password = request.POST['password']
            pw_conf = request.POST['pw_conf']
            user.save()
            messages.add_message(request, messages.INFO, 'Info successfully updated')
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
            return redirect('/')

        if bcrypt.checkpw(password.encode(), user.password.encode()):
            request.session['curr_user_id'] = user.id
            return redirect('/success')

def logout(request):
    request.session['curr_user_id'] = 'none'
    return redirect('/signin')