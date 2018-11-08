from django.db import models

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


# class Seat_Chart(models.Model):
#     train = models.ForeignKey(Train, on_delete=models.CASCADE, related_name="train_chart")
#     first_ac = models.IntegerField("1st AC")
#     second_ac = models.IntegerField("2nd AC")
#     third_ac = models.IntegerField("3rd AC")
#     sleeper = models.IntegerField("Sleeper")
#     date = models.DateTimeField
