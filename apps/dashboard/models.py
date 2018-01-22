# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from ..users.models import *
from django.db import models
'''
below is untested and has not been migrated.
'''
class Post(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    post_maker = models.ForeignKey(User, related_name='posts_made')
    post_receiver = models.ForeignKey(User, related_name='posts_received')

class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    post = models.ForeignKey(Post, related_name='comments')
    comment_maker = models.ForeignKey(User, related_name='comments_made')