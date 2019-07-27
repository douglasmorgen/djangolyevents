from django.contrib import admin



# Register your models here.
from .models import Event
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display=['eventname','date']