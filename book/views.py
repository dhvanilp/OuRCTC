from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from dateutil import parser
import json, time

# Create your views here.

@login_required(login_url="/login")
def homeView(request):
    stations=Station.objects.all()
    context={
        "stations" : stations,
        "st" : stations[0:4]
    }
    return render(request,'book/home.html',context)

@login_required(login_url="/login")
def searchView(request):
    source = Station.objects.get(pk=request.POST['source'])
    dest = Station.objects.get(pk=request.POST['dest'])
    date = request.POST['journey_date']
    sourceTrains = []
    for s in source.station_schedule.all():
        sourceTrains.append(s.train)
    destTrains = []
    for s in dest.station_schedule.all():
        destTrains.append(s.train)
    allTrains=list(set(sourceTrains) & set(destTrains))

    trains=[]
    sourceSchedules=[]
    destSchedules=[]
    scheduleCharts=[]
    for t in allTrains:
        departing_station = t.train_schedule.get(station=source)
        arriving_station = t.train_schedule.get(station=dest)
        if departing_station.pk < arriving_station.pk:
            scheduleCharts.append(Seat_Chart.objects.get(date=parser.parse(date),train=t))
            trains.append(t)
            sourceSchedules.append(departing_station)
            destSchedules.append(arriving_station)

    schedules=zip(trains,sourceSchedules,destSchedules,scheduleCharts)
    data={
        "source": source,
        "dest": dest,
        "schedules":schedules,
        "date": date,
    }
    return render(request,'book/trainSearch.html',data)

@login_required(login_url="/login")
def bookView(request,chart,sourceSchedule,destSchedule,type,date):
    chart = Seat_Chart.objects.get(pk=chart)
    train = chart.train
    sourceSchedule=Schedule.objects.get(pk=sourceSchedule)
    destSchedule=Schedule.objects.get(pk=destSchedule)
    source = sourceSchedule.station
    dest = destSchedule.station
    data = {
        "train": train,
        "chart": chart,
        "sourceSchedule": sourceSchedule,
        "destSchedule": destSchedule,
        "source":source,
        "dest":dest,
        "type":type,
        "date":date,
    }
    return render(request,'book/booking.html',data)

@login_required(login_url="/login")
def confirmTicketView(request,chart,sourceSchedule,destSchedule,type,date):
    chart=Seat_Chart.objects.get(pk=chart)
    train=chart.train
    sourceSchedule=Schedule.objects.get(pk=sourceSchedule)
    destSchedule=Schedule.objects.get(pk=destSchedule)
    source = sourceSchedule.station
    dest = destSchedule.station
    user= request.user
    seats=int(request.POST["seats"])
    for i in range(seats):
        name=request.POST.get("name"+str(i))
        b=Ticket()
        b.passenger=name
        b.train=train
        b.type=type
        b.chart=chart
        b.user=user
        b.source=source
        b.dest=dest
        b.source_schedule=sourceSchedule
        b.dest_schedule=destSchedule
        b.date = date
        b.save()


    data = {
        "train": train,
        "sourceSchedule": sourceSchedule,
        "destSchedule": destSchedule,
        "source":source,
        "dest":dest,
        "type":type
    }
    return render(request, 'book/home.html')

@login_required(login_url="/login")
def profileView(request):
    user=request.user
    booked=user.tickets.all()
    data={
        "booked":booked,
    }
    return render(request, 'book/profile.html',data)

class cancelTicket(LoginRequiredMixin, DeleteView):
    login_url = '/login'
    model = Ticket
    success_url = reverse_lazy('book:profile')

    def dispatch(self, request, *args, **kwargs):
        pk=kwargs['pk']
        if request.user != Ticket.objects.get(pk=pk).user:
            return redirect('book:home')
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)



# json_data = open('static/railways/stations.json','r')
# stations = json.loads(json_data.read())
# for d in stations["features"]:
#     data = d["properties"]
#     station = Station()
#     station.state = data["state"]
#     station.code = data["code"]
#     station.name = data["name"]
#     station.zone = data["zone"]
#     station.address = data["address"]
#     station.save()

# json_data = open('static/railways/trains.json', 'r')
# trains = json.loads(json_data.read())
# for d in trains["features"]:
#     data = d["properties"]
#     train = Train()
#     train.arrival = data["arrival"]
#     train.source = Station.objects.get(pk=data["from_station_code"])
#     train.name = data["name"]
#     train.number = data["number"]
#     train.departure = data["departure"]
#     train.return_train = data["return_train"]
#     train.dest = Station.objects.get(pk=data["to_station_code"])
#     train.duration_m = data["duration_m"]
#     train.duration_h = data["duration_h"]
#     train.type = data["type"]
#     train.distance = data["distance"]
#     print(train)
#     train.save()
#
# json_data = open('static/railways/schedules.json', 'r')
# schedules = json.loads(json_data.read())
# for data in schedules:
#     schedule = Schedule()
#     schedule.arrival = data["arrival"]
#     schedule.day = data["day"]
#     schedule.station = Station.objects.get(pk=data["station_code"])
#     schedule.train = Train.objects.get(pk=data["train_number"])
#     schedule.departure = data["departure"]
#     schedule.id = data["id"]
#     print(schedule.id)
#     schedule.save()
