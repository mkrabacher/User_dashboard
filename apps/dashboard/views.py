# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
import bcrypt
from django.contrib import messages
from django.shortcuts import render, redirect
from ..users.models import *
from models import *

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

def createPost(request):
	if request.method == 'POST':
		content = str(request.POST['post'])
		maker_id = str(request.POST['poster_id'])
		receiver_id = str(request.POST['receiver_id'])

		Post.objects.create(content=content, post_receiver=User.objects.get(id=receiver_id), post_maker=User.objects.get(id=maker_id))
		return redirect('/dashboard/show/'+receiver_id)

def createComment(request):
	if request.method == 'POST':
		content = str(request.POST['comment'])
		post_id = str(request.POST['post_id'])
		commenter_id = str(request.POST['commenter_id'])

		Comment.objects.create(content=content, post=Post.objects.get(id=post_id), comment_maker=User.objects.get(id=commenter_id))
		return redirect('/dashboard/show/'+str(Post.objects.get(id=post_id).post_receiver.id))
	