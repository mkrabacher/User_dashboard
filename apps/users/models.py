# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re
from datetime import *


class UserManager(models.Manager):
    def validate(self, postData):
        errors = {}

        if len(postData['fName']) < 2:
            errors['fName'] = 'You gotta have a longer first name, bruh.'
            
        if len(postData['lName']) < 2:
            errors['lName'] = 'You gotta have a longer last name, bruh.'

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        try:
            User.objects.get(email=postData['email'])
            errors['email'] = 'Email already taken. Be more creative than you are.'
        except:
            if not EMAIL_REGEX.match(postData['email']):
                errors['email'] = 'You gotta have a valid email, bruh.'

        if datetime.strptime(postData['birthday'], '%Y-%m-%d') > datetime.now():
            errors['birthday'] = "That date hasn't happen yet. So wtf are you doing puttin it in as your b-day."

        if postData['password'] != postData['pw_conf']:
            errors['passwordMatch'] = 'You gotta have a longer last name, bruh.'
        if len(postData['password']) < 8:
            errors['password'] = 'You gotta have a longer pw, bruh.'

        return errors

    def validateInfo(self, postData):
        errors = {}

        if len(postData['fName']) < 2:
            errors['fName'] = 'You gotta have a longer first name, bruh.'
            
        if len(postData['lName']) < 2:
            errors['lName'] = 'You gotta have a longer last name, bruh.'

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if User.objects.get(email=postData['email']):
            errors['email'] = 'Email already taken. Be more creative than you are.'
        elif not EMAIL_REGEX.match(postData['email']):
            errors['email'] = 'You gotta have a valid email, bruh.'

        if datetime.strptime(postData['birthday'], '%Y-%m-%d') > datetime.now():
            errors['birthday'] = "That date hasn't happen yet. So wtf are you doing puttin it in as your b-day."

        return errors

    def validatePW(self, postData):
        errors = {}
        if postData['password'] != postData['pw_conf']:
            errors['passwordMatch'] = 'You gotta have a longer last name, bruh.'
        if len(postData['password']) < 8:
            errors['password'] = 'You gotta have a longer pw, bruh.'

        return errors

class User(models.Model):
    fName = models.CharField(max_length=255)
    lName = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    birthday = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    password = models.CharField(max_length=255)
    desc = models.TextField()
    level =  models.CharField(max_length=6)
    objects = UserManager()

    # def __str__(self):
    #     return self.fName, self.lName