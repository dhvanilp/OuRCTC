from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Station)
admin.site.register(Train)
admin.site.register(Schedule)
admin.site.register(Seat_Chart)
admin.site.register(Ticket          )
