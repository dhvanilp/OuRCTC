from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import *
import json, time


# Create your views here.

@login_required(login_url="/login")
def homeView(request):
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

    json_data = open('static/railways/schedules.json', 'r')
    schedules = json.loads(json_data.read())
    for data in schedules:
        schedule = Schedule()
        schedule.arrival = data["arrival"]
        schedule.day = data["day"]
        schedule.station = Station.objects.get(pk=data["station_code"])
        schedule.train = Train.objects.get(pk=data["train_number"])
        schedule.departure = data["departure"]
        schedule.id = data["id"]
        print(schedule.id)
        schedule.save()

    return render(request,'book/home.html')

@login_required(login_url="/login")
def searchView(request):
    data={
        "source" : request.POST['source'],
        "dest" :request.POST['dest']
    }
    return render(request,'book/search.html',data)