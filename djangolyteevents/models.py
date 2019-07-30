from django.db import models
from django.utils.timezone import now
from decimal import Decimal
import django_filters

#from . import serializers
#from .serializers import EventSerializer

# Create your models here.
class Event(models.Model):
    #STATUS_CHOICES=[('D','draft'),('L','live'),('S','started'),('E','ended'),('CO','completed'),('CA','canceled')]
    name=models.CharField(max_length=255)
    summary=models.TextField()
    description=models.TextField()
    url=models.URLField()
    external_id=models.CharField(max_length=255,unique=True)
    
    start = models.DateTimeField(default=now, blank=True)
    end = models.DateTimeField(default=now, blank=True)
    created=models.DateTimeField(default=now, blank=True)
    changed=models.DateTimeField(default=now, blank=True)
    published=models.DateTimeField(default=now, blank=True)
    status= models.CharField(max_length=255, blank=True)
    currency=models.CharField(max_length=3,default='USD')
    online_event=models.BooleanField(default=True)
    hide_start_date=models.BooleanField(default=True)
    hide_end_date=models.BooleanField(default=True)
    organizer_name=models.CharField(max_length=255, blank=True,null=True)
    organizer_description=models.TextField(blank=True,null=True)
    is_free=models.BooleanField(default=True)
    has_available_tickets=models.BooleanField(default=True)
    
    minimum_ticket_price = models.DecimalField(max_digits=8, decimal_places=2,default=Decimal('0.0000'))
    maximum_ticket_price = models.DecimalField(max_digits=8, decimal_places=2,default=Decimal('0.0000'))

    def __str__(self):
        return "%s %s" % (self.name,self.start)



class EventFilterVerbose(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name',lookup_expr='icontains')
    organizer_name = django_filters.CharFilter(field_name='organizer_name',lookup_expr='icontains')
    minimum_ticket_price__gt = django_filters.NumberFilter(field_name='minimum_ticket_price', lookup_expr='gt')
    minimum_ticket_price__lt = django_filters.NumberFilter(field_name='minimum_ticket_price', lookup_expr='lt')
    maximum_ticket_price__lt = django_filters.NumberFilter(field_name='maximum_ticket_price', lookup_expr='lt')
    maximum_ticket_price__gt = django_filters.NumberFilter(field_name='maximum_ticket_price', lookup_expr='gt')
    start__gt = django_filters.DateTimeFilter(field_name='start', lookup_expr='gte')
    start__lt = django_filters.DateTimeFilter(field_name='start', lookup_expr='lte')

    class Meta:
        model = Event
        fields = ['name','organizer_name','minimum_ticket_price','maximum_ticket_price', 'start']


class EventFilter(django_filters.FilterSet):
    class Meta:
        model = Event
        fields = {
            'name':['icontains'],
            'minimum_ticket_price': ['gt',],
            'maximum_ticket_price': ['lt',],
            'start': ['exact', 'year__gt'],
        }


#integrate these into app
# class ProductFilter(filters.FilterSet):
#     min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
#     max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')

#     class Meta:
#         model = Product
#         fields = ['category', 'in_stock', 'min_price', 'max_price']



# class ProductFilter(django_filters.FilterSet):
#     price = django_filters.NumberFilter()
#     price__gt = django_filters.NumberFilter(field_name='price', lookup_expr='gt')
#     price__lt = django_filters.NumberFilter(field_name='price', lookup_expr='lt')

#     release_year = django_filters.NumberFilter(field_name='release_date', lookup_expr='year')
#     release_year__gt = django_filters.NumberFilter(field_name='release_date', lookup_expr='year__gt')
#     release_year__lt = django_filters.NumberFilter(field_name='release_date', lookup_expr='year__lt')

#     manufacturer__name = django_filters.CharFilter(lookup_expr='icontains')

#     class Meta:
#         model = Product        

    #def create_from_api(self,event):
        

#         name 	multipart-text 	Event name.
# summary 	string 	(Optional) Event summary. Short summary describing the event and its purpose.
# description 	multipart-text 	(Optional) Event description. Description can be lengthy and have significant formatting.
# url 	string 	URL of the Event's Listing page on eventbrite.com.
# start 	datetime-tz 	Event start date and time.
# end 	datetime-tz 	Event end date and time.
# created 	datetime 	Event creation date and time.
# changed 	datetime 	Date and time of most recent changes to the Event.
# published 	datetime 	Event publication date and time.
# status 	string 	Event status. Can be draft, live, started, ended, completed and canceled.
# currency 	string 	Event ISO 4217 currency code.
# online_event 	boolean 	true = Specifies that the Event is online only (i.e. the Event does not have a Venue).
# hide_start_date 	boolean 	If true, the event's start date should never be displayed to attendees.
# hide_end_date 	boolean 	If true, the event's end date should never be displayed to attendees.