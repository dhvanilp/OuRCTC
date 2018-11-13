from django.urls import path

from . import views

app_name = 'book'

urlpatterns = [
    path('',views.homeView,name="home"),
    path('search',views.searchView,name="search"),
    path('complexSearch/<source>-<dest>/<date>',views.complexSearchView,name="complexSearch"),
    path('mapSearch>',views.MapSearchView.as_view(),name="mapSearch"),
    path('book/<chart>/<sourceSchedule>-<destSchedule>/<type>/<date>',views.bookView,name="book"),
    path('book/<chart1>-<chart2>/<sourceSchedule>-<commonSchedule1>/<commonSchedule2>-<destSchedule>/<type>/<date>',views.complexBookView,name="complexBook"),
    path('confirm/<chart>/<sourceSchedule>-<destSchedule>/<type>/<date>',views.confirmTicketView,name="confirm"),
    path('confirm/<chart1>-<chart2>/<sourceSchedule>-<commonSchedule1>/<commonSchedule2>-<destSchedule>/<type>/<date>',views.complexConfirmTicketView,name="complexConfirm"),
    path('profile', views.profileView, name="profile"),
    path('cancel/<pk>', views.cancelTicket.as_view(), name="cancel"),


]
