# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import *
from django.core.urlresolvers import reverse

def index(response):
    return render(response, "review_app/index.html")

def register(request):
    if User.userManager.isValidRegistration(request.POST, request):
        passFlag = True
        user1 = User.objects.get(email=request.POST['email'])
        request.session['user']=user1.id
        return render(request,"review_app/books.html")
    else:
        passFlag = False
        return redirect(reverse('index'))

# def success(request):
#     return render(request, 'review_app/books.html')

def login(request):
    if User.userManager.UserExistsLogin(request.POST, request):
        passFlag = True
        user1 = User.objects.get(email=request.POST['email'])
        request.session['user']=user1.id
        return redirect("/books")  #redirect (reverse('books'))
    else:
        passFlag = False
        return redirect (reverse('index'))
# Create your views here.

def books(request):
    return render(request, "review_app/books.html")

def add(request):
    return render(request, "review_app/add.html")

def create(request):
    title = request.POST['book_title']
    
    if request.POST['new_author'] == '':
        author= request.POST['new_author']
    else:
        author=request.POST['author_list']
    book_one = Book.objects.create(title = title, author= author) 
    print request.session.items()
    Review.objects.create(review = request.POST['review'], rating = int(request.POST['rating']), book_id=book_one.id, user_id=request.session['user'])
    return redirect('/books/'+ str(book_one.id))

def profile(request, id):
    return render(request, 'review_app/book_profile.html')


