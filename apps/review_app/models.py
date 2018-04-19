# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

import bcrypt
import re
from django.contrib import messages

EMAIL_REGEX = re.compile (r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def isValidRegistration(self, userInfo, request):
        passFlag = True
        if not userInfo['name'].isalpha():
            messages.warning(request, 'First name contains non-alpha characters.')
            passFlag = False
        if len(userInfo['name']) < 2:
            messages.warning(request, 'First name is too short.')
            passFlag = False
        if not userInfo['alias'].isalpha():
            messages.warning(request, 'Last name contains non-alpha characters.')
            passFlag = False
        if len(userInfo['alias']) < 2:
            messages.warning(request, 'Last name is too short.')
            passFlag = False
        if not EMAIL_REGEX.match(userInfo['email']):
            messages.warning(request, 'Email is not vaild!')
            passFlag = False
        if len(userInfo['password']) < 8:
            messages.warning(request, 'Password is too short.')
            passFlag = False
        if userInfo['password'] != userInfo['confirm_password']:
            messages.warning(request, "The passwords you've entered do not match.")
            passFlag = False
        if User.objects.filter(email = userInfo['email']):
			messages.error(request, "This email already exists in our database.")
			passFlag = False

        if passFlag == True:
            messages.success(request, "Success! Welcome, " + userInfo['name'] + "!")
            hashed = bcrypt.hashpw(userInfo['password'].encode(), bcrypt.gensalt())
            User.objects.create(name = userInfo['name'], alias = userInfo['alias'], email = userInfo['email'], password = hashed)
        return passFlag

    def UserExistsLogin(self, userInfo, request):
        passFlag = True
        if User.objects.filter(email = userInfo['email']):
            hashed = User.objects.get(email = userInfo['email']).password
            hashed = hashed.encode('utf-8')
            password = userInfo['password']
            password = password.encode('utf-8')
            if bcrypt.hashpw(password, hashed) == hashed:
                messages.success(request, "Success! Welcome, " + User.objects.get(email = userInfo['email']).name + "!")
                passFlag = True
            else:
                messages.warning(request, "Unsuccessful login. Incorrect password")
                passFlag = False
        else:
            messages.warning(request, "Your email is incorrect or not in our database.")
            passFlag = False
        return passFlag

class User(models.Model):
    name = models.CharField(max_length = 255)
    alias = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    userManager = UserManager()
    objects = models.Manager()

class Book(models.Model):
    title = models.CharField(max_length = 255)
    author = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Review(models.Model):
    rating = models.IntegerField()
    review = models.TextField()
    user = models.ForeignKey(User, related_name = "reviews")
    book = models.ForeignKey(Book, related_name = "reviews")
