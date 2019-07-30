from rest_framework import serializers
from djangolyteevents import models
from .models import Event

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Event
        fields = ('id', 'name','summary','url','external_id','start','end','created','changed','published','status',
        'currency','online_event','hide_start_date','hide_end_date','organizer_name','organizer_description','is_free','has_available_tickets',
        'minimum_ticket_price','maximum_ticket_price',
        )
        