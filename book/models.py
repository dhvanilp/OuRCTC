from django.db import models
from django.contrib.auth import get_user_model

User= get_user_model()


# Create your models here.

class Station(models.Model):
    state = models.CharField("State",max_length=20, null=True)
    code = models.CharField("Code",max_length=10,primary_key=True)
    name = models.CharField("Name",max_length=30)
    zone = models.CharField("Zone",max_length=10, null=True)
    address = models.CharField("Address",max_length=50, null=True)

    def __str__(self):
        return self.name

class Train(models.Model):
    arrival = models.CharField("Arrival",max_length=8, null=True)
    source = models.ForeignKey(Station, on_delete=models.SET(None), related_name="train_source")
    name = models.CharField("Name", max_length=30)
    zone = models.CharField("Zone", max_length=10, null=True)
    number = models.CharField("Number", max_length=15,primary_key=True)
    departure = models.CharField("Departure",max_length=8, null=True)
    return_train = models.CharField("Return Train",max_length=15, null=True)
    dest = models.ForeignKey(Station, on_delete=models.SET(None), related_name="train_dest")
    duration_h = models.IntegerField("Duration Hours", null=True)
    duration_m = models.IntegerField("Duration Minutes", null=True)
    type = models.CharField("Type",max_length=5, null=True)
    distance = models.IntegerField("Distance", null=True)

    def __str__(self):
        return self.name


class Schedule(models.Model):
    arrival = models.CharField("Arrival", max_length=8, null=True)
    day = models.IntegerField("Day", null=True)
    train = models.ForeignKey(Train, on_delete=models.CASCADE, related_name="train_schedule")
    station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name="station_schedule")
    id = models.IntegerField("id",primary_key=True)
    departure = models.CharField("Departure", max_length=8, null=True)

    def __str__(self):
        return str(self.train) +" at "+str(self.station)


class Seat_Chart(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE, related_name="train_chart")
    first_ac = models.IntegerField("1st AC")
    second_ac = models.IntegerField("2nd AC")
    third_ac = models.IntegerField("3rd AC")
    sleeper = models.IntegerField("Sleeper")
    date = models.DateField("Date")

    def get1A(self):
        return self.first_ac - self.chart_tickets.all().filter(type="1A").count()

    def get2A(self):
        return self.second_ac - self.chart_tickets.all().filter(type="2A").count()

    def get3A(self):
        return self.third_ac - self.chart_tickets.all().filter(type="3A").count()

    def getSL(self):
        return self.sleeper - self.chart_tickets.all().filter(type="SL").count()

    def __str__(self):
        return str(self.train) +" on "+str(self.date)

class Ticket(models.Model):
    passenger = models.CharField("Name",max_length=20)
    train = models.ForeignKey(Train, on_delete=models.CASCADE, related_name="train_tickets")
    type = models.CharField("Type",max_length=2)
    chart = models.ForeignKey(Seat_Chart, on_delete=models.CASCADE, related_name="chart_tickets")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tickets")
    source = models.ForeignKey(Station, on_delete=models.CASCADE, related_name="source_tickets")
    dest = models.ForeignKey(Station, on_delete=models.CASCADE, related_name="dest_tickets")
    source_schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name="source_schedule_tickets")
    dest_schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name="dest_schedule_tickets")
    date = models.DateField("Date")
    fare = models.IntegerField("Fare")

    def __str__(self):
        return str(self.passenger) +" on "+str(self.date)+" in "+str(self.train)

    def calculateFare(self):
        factor=1
        if(self.type=="1A"):
            factor=20
        elif(self.type=="2A"):
            factor=15
        elif (self.type == "3A"):
            factor = 10
        else:
            factor = 5
        self.fare = (self.dest_schedule.pk - self.source_schedule.pk)*factor
