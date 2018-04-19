from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name ="index"),
    url(r'^register$', views.register, name = "register"),
    # url(r'^success$', views.success, name = "success"),
    url(r'^login$', views.login, name = "login"),
    url(r'^books$', views.books, name = "books"),
    url(r'^books/add$', views.add, name = "add"),
    url(r'^book/create$', views.create),
    url(r'^books/(?P<id>\d+)$', views.profile),

    # url(r'^books$', views.books, name = "books"),
]