# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
import bcrypt
from django.contrib import messages
from django.shortcuts import render, redirect
from ..users.models import *

def index(request):
	return render(request, 'dashboard/index.html')

def success(request):
    if request.session['curr_user_id'] != 'none':
        return redirect('/dashboard/show/' + str(request.session['curr_user_id']))
    
    return redirect('/signin')

def show(request, number):
	if request.session['curr_user_id'] == 'none':
		return redirect('/signin')

	context = {
		'user':User.objects.get(id=number),
		'curr_user':User.objects.get(id=request.session['curr_user_id'])
	}
	return render(request, 'dashboard/show.html', context)
	
def showAll(request):
	if request.session['curr_user_id'] == 'none':
		return redirect('/signin')

	context = {
		'users':User.objects.all(),
		'curr_user':User.objects.get(id=request.session['curr_user_id'])
	}
	return render(request, 'dashboard/all.html', context)
	