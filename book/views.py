from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import *
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
    for t in allTrains:
        departing_station = t.train_schedule.get(station=source)
        arriving_station = t.train_schedule.get(station=dest)
        if departing_station.pk < arriving_station.pk:
            trains.append(t)
            sourceSchedules.append(departing_station)
            destSchedules.append(arriving_station)


    schedules=zip(trains,sourceSchedules,destSchedules)
    data={
        "source": source,
        "dest": dest,
        "schedules":schedules
    }
    return render(request,'book/trainSearch.html',data)

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
