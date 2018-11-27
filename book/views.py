from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import authentication, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
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
    fares=[]
    for t in allTrains:
        departing_station = t.train_schedule.get(station=source)
        arriving_station = t.train_schedule.get(station=dest)
        if departing_station.pk < arriving_station.pk:
            scheduleCharts.append(Seat_Chart.objects.get(date=parser.parse(date),train=t))
            trains.append(t)
            sourceSchedules.append(departing_station)
            destSchedules.append(arriving_station)
            fare={}
            fare["1A"]=(arriving_station.pk - departing_station.pk)*20
            fare["2A"]=(arriving_station.pk - departing_station.pk)*15
            fare["3A"]=(arriving_station.pk - departing_station.pk)*10
            fare["SL"]=(arriving_station.pk - departing_station.pk)*5
            fares.append((fare))

    schedules=zip(trains,sourceSchedules,destSchedules,scheduleCharts,fares)
    data={
        "source": source,
        "dest": dest,
        "schedules":schedules,
        "date": date,
    }
    return render(request,'book/trainSearch.html',data)

@login_required(login_url="/login")
def complexSearchView(request,source,dest,date):
    source = Station.objects.get(pk=source)
    dest = Station.objects.get(pk=dest)
    sourceTrains = []
    for s in source.station_schedule.all():
        sourceTrains.append(s.train)
    destTrains = []
    for s in dest.station_schedule.all():
        destTrains.append(s.train)
    # allTrains=list(set(sourceTrains) & set(destTrains))

    trains1 = []
    trains2 = []
    sourceSchedules = []
    commonSchedules1 = []
    commonSchedules2 = []
    destSchedules = []
    scheduleCharts1 = []
    scheduleCharts2 = []
    fares=[]


    for ts in sourceTrains:
        sourceSchedule=source.station_schedule.get(train=ts)
        source_stations = []
        for a in ts.train_schedule.filter(id__gte=sourceSchedule.id):
            source_stations.append(a.station)
        for td in destTrains:
            destSchedule = dest.station_schedule.get(train=td)
            dest_stations = []
            for a in td.train_schedule.filter(id__lte=destSchedule.id):
                dest_stations.append(a.station)
            common = list(set(source_stations) & set(dest_stations))
            for c in common:
                tempDestSchedule=c.station_schedule.get(train=ts)
                tempSourceSchedule=c.station_schedule.get(train=td)
                if(tempDestSchedule.arrival < tempSourceSchedule.departure):
                    trains1.append(ts)
                    trains2.append(td)
                    commonSchedules1.append(tempDestSchedule)
                    commonSchedules2.append(tempSourceSchedule)
                    sourceSchedules.append(sourceSchedule)
                    destSchedules.append(destSchedule)
                    c1=Seat_Chart.objects.get(date=parser.parse(date),train=ts)
                    c2=Seat_Chart.objects.get(date=parser.parse(date),train=td)
                    scheduleCharts1.append(c1)
                    scheduleCharts2.append(c2)
                    # fares.append(None)
                    fare = {}
                    fare["1A"] = (destSchedule.pk - tempSourceSchedule.pk + tempDestSchedule.pk - sourceSchedule.pk) * 20
                    fare["2A"] = (destSchedule.pk - tempSourceSchedule.pk + tempDestSchedule.pk - sourceSchedule.pk) * 15
                    fare["3A"] = (destSchedule.pk - tempSourceSchedule.pk + tempDestSchedule.pk - sourceSchedule.pk) * 10
                    fare["SL"] = (destSchedule.pk - tempSourceSchedule.pk + tempDestSchedule.pk - sourceSchedule.pk) * 5
                    fares.append((fare))
                    break

    schedules=zip(trains1,trains2,sourceSchedules,commonSchedules1,commonSchedules2,destSchedules,scheduleCharts1,scheduleCharts2,fares)
    data={
        "source": source,
        "dest": dest,
        "schedules":schedules,
        "date": date,
    }
    return render(request,'book/connectingTrainSearch.html',data)


class MapSearchView(LoginRequiredMixin, APIView):
    login_url =  '/login'
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        date=request.GET["date"]
        sources = request.GET["source"]
        dests = request.GET["dest"]
        for s in sources:
            source=Station.objects.filter(name__iexact=sources)
            print(s)
            if source.count():
                break
        for d in dests:
            dest=Station.objects.filter(name__iexact=dests)
            if dest.count():
                break

        data={
            "date":date,
            "source":source[0].code,
            "dest": dest[0].code,
        }

        return Response(data)

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
def complexBookView(request,chart1,chart2,sourceSchedule,commonSchedule1,commonSchedule2,destSchedule,type,date):
    chart1 = Seat_Chart.objects.get(pk=chart1)
    chart2 = Seat_Chart.objects.get(pk=chart2)
    train1 = chart1.train
    train2 = chart2.train
    sourceSchedule=Schedule.objects.get(pk=sourceSchedule)
    commonSchedule1=Schedule.objects.get(pk=commonSchedule1)
    commonSchedule2=Schedule.objects.get(pk=commonSchedule2)
    destSchedule=Schedule.objects.get(pk=destSchedule)
    source = sourceSchedule.station
    dest = destSchedule.station
    data = {
        "train1": train1,
        "train2": train2,
        "chart1": chart1,
        "chart2": chart2,
        "sourceSchedule": sourceSchedule,
        "commonSchedule1": commonSchedule1,
        "commonSchedule2": commonSchedule2,
        "destSchedule": destSchedule,
        "source":source,
        "dest":dest,
        "type":type,
        "date":date,
    }
    return render(request,'book/complexBooking.html',data)

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
        b.calculateFare()
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
def complexConfirmTicketView(request,chart1,chart2,sourceSchedule,commonSchedule1,commonSchedule2,destSchedule,type,date):
    chart1 = Seat_Chart.objects.get(pk=chart1)
    chart2 = Seat_Chart.objects.get(pk=chart2)
    train1 = chart1.train
    train2 = chart2.train
    sourceSchedule = Schedule.objects.get(pk=sourceSchedule)
    commonSchedule1 = Schedule.objects.get(pk=commonSchedule1)
    commonSchedule2 = Schedule.objects.get(pk=commonSchedule2)
    destSchedule = Schedule.objects.get(pk=destSchedule)
    source = sourceSchedule.station
    dest = destSchedule.station
    user= request.user
    seats=int(request.POST["seats"])
    for i in range(seats):
        name=request.POST.get("name"+str(i))
        b=Ticket()
        b.passenger=name
        b.train=train1
        b.type=type
        b.chart=chart1
        b.user=user
        b.source=source
        b.dest=dest
        b.source_schedule=sourceSchedule
        b.dest_schedule=commonSchedule1
        b.date = date
        b.calculateFare()
        b.save()

        b = Ticket()
        b.passenger = name
        b.train = train2
        b.type = type
        b.chart = chart2
        b.user = user
        b.source = source
        b.dest = dest
        b.source_schedule = commonSchedule2
        b.dest_schedule = destSchedule
        b.date = date
        b.calculateFare()
        b.save()


    data = {
        "train1": train1,
        "train2": train2,
        "chart1": chart1,
        "chart2": chart2,
        "sourceSchedule": sourceSchedule,
        "commonSchedule1": commonSchedule1,
        "commonSchedule2": commonSchedule2,
        "destSchedule": destSchedule,
        "source":source,
        "dest":dest,
        "type":type,
        "date":date,
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
