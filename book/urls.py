from django.urls import path

from . import views

app_name = 'book'

urlpatterns = [
    path('',views.homeView,name="home"),
    path('search',views.searchView,name="search"),
    path('book/<chart>/<sourceSchedule>-<destSchedule>/<type>/<date>',views.bookView,name="book"),
    path('confirm/<chart>/<sourceSchedule>-<destSchedule>/<type>/<date>',views.confirmTicketView,name="confirm"),
    path('profile', views.profileView, name="profile"),
    path('cancel/<pk>', views.cancelTicket.as_view(), name="cancel"),


]
