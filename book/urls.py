from django.urls import path

from . import views

app_name = 'book'

urlpatterns = [
    path('',views.homeView,name="home"),
    path('/search',views.searchView,name="search"),

]
