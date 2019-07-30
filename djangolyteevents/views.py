from django.shortcuts import render
from .models import Event
from .models import EventFilter
from .models import EventFilterVerbose
from django.http import HttpResponse,HttpResponseBadRequest,HttpResponseNotFound
from django.http import JsonResponse
import requests
import json
from requests_oauthlib import OAuth2Session
from rest_framework.response import Response
from rest_framework import viewsets
from . import serializers
from . import models
import django_filters
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from .serializers import EventSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.conf import settings
EVENTBRITE_CLIENT_ID="4GQQFB6MUA5Y2RNBIQ55"
EVENTBRITE_CLIENT_SECRET="C5JPYH3P6XGF5G6D5PEGXHLZTQPVQISY7VCIGWE5L7WQT4WFK5"
EVENTBRITE_TOKEN='4GQQFB6MUA5Y2RNBIQ55'

# class EventViewset(viewsets.ModelViewSet):
    
#     queryset = models.Event.objects.all()

#     serializer_class = serializers.EventSerializer
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['name', 'url']
    # filter_backends = (filters.DjangoFilterBackend, SearchFilter, OrderingFilter)
    # filter_fields = __basic_fields
    # search_fields = __basic_fields

# class EventList(generics.ListAPIView):
#     queryset = Event.objects.all()
#     serializer_class = EventSerializer
#     filter_backends = (filters.DjangoFilterBackend,)
#     filterset_class = EventFilter        

class EventList(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = EventFilterVerbose

#@api_view(['GET','PUT'])
# def EventUpdate(request, external_id):
#     """
#     Retrieve, update or delete a code snippet.
#     """
#     try:
#         event = Event.objects.get(external_id)
#     except Event.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = EventSerializer(event)
#         return Response(serializer.data)

#     elif request.method == 'PUT':
#         serializer = EventSerializer(event, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET', 'PUT'])
def EventUpdate(request,external_id):
    if request.method == 'GET':
        try:
            event_update=Event.objects.get(external_id=external_id)
        except Event.DoesNotExist:
            return HttpResponseNotFound('<h1>Event not found</h1>')
        
        serializer = EventSerializer(event_update)
        return JsonResponse(serializer.data)
    elif request.method == 'PUT':    
        
        try:
            event_update=Event.objects.get(external_id=external_id)
        except Event.DoesNotExist:
            return HttpResponseNotFound('<h1>Event not found</h1>')   
        serializer = EventSerializer(event_update,data=request.data)
        #serializer.update()
        if serializer.is_valid():
            serializer.save()
            #return HttpResponse("You updated id " + external_id)
        #   content = JSONRenderer().render(serializer.data)
            return JsonResponse(serializer.data)
            #return HttpResponse("save attempted")
        else:
            return HttpResponseBadRequest('<h1>Bad Request</h1>')
        

def index(request):
    return HttpResponse("Hello, world. You're at my coding challenge.")

def fill_db(request,pages,fill,start_page):
    # This information is from eventbrite
    client_id = EVENTBRITE_CLIENT_ID
    client_secret = EVENTBRITE_CLIENT_SECRET
    if pages > 6:
        pages=6
    if fill==1:
        filldb=True
    else:
        filldb=False
    #authorization_base_url = 'https://www.eventbrite.comunique field django/oauth/authorize'
    token_url = 'https://www.eventbrite.com/oauth/token'
    api_url='https://www.eventbriteapi.com/v3/events/search/'
    
    from oauthlib.oauth2 import BackendApplicationClient
    client = BackendApplicationClient(client_id=client_id)
    oauth = OAuth2Session(client=client)
    #token = oauth.fetch_token(token_url=token_url, client_id=client_id, client_secret=client_secret)
    token=EVENTBRITE_TOKEN
    api_url_with_token=api_url+'?token='+token
    head = {'Authorization': 'token {}'.format(token)}
    #response = oauth.get(api_url, headers=head)

    #response = requests.get(api_url, headers={'Authorization': 'access_token myToken'})
    
    #events=json.loads(oauth.get(api_url_with_token).json())
    #events=oauth.get(api_url_with_token).json()
    
    pagecount=start_page
    token='4GQQFB6MUA5Y2RNBIQ55'
    description=''
    expansion="&expand=ticket_classes"
    expansion="&price=paid"
    expansion="&expand=expand=ticket_availability"
    upper_limit=pagecount+pages
    while pagecount<upper_limit and filldb:
        api_url_with_token=api_url+'?token='+token+'&page='+str(pagecount)

        events=oauth.get(api_url_with_token).json()
        event0json=events['events'][0];
        
        
        object_count=events['pagination']["object_count"]
        page_number=events['pagination']['page_number']
        page_size=events['pagination']["page_size"]
        page_count=events['pagination']["page_count"]
        has_more_items=events['pagination']["has_more_items"]

    # "object_count": 72201,
    # "page_number": 1,
    # "page_size": 50,
    # "page_count": 200,
    # "has_more_items": true
        for event in events['events']:
            if event['description']['html'] is None:
                description=description+"<br>NO HTML<BR>"
            else:    
                description=description+'<br>event id: <br>'+event['id']+'<br>'+ event['description']['html']
                

                kwargs={"name": event['name']['text'],"summary": event['summary'],"description":event['description']['html'],
                    "url":event['url'],"start":event['start']['utc'],"end":event['end']['utc'],
                    "created":event['created'],"changed":event['changed'],"published":event['published'],"status":event['status'],
                    "currency":event['currency'],"online_event":event['online_event'],
                    "hide_start_date":event['hide_start_date'],"hide_end_date":event['hide_end_date'],"is_free":event['is_free'],}

                #if event['id']=='61980656813' and Event.objects.filter(external_id=event['id']).exists() and event['is_free']==False:
                if  Event.objects.filter(external_id=event['id']).exists():

                    #get the event ticket details and organizer details
                    
                    event_api_url="https://www.eventbriteapi.com/v3/events/"+event['id']+"/?expand=organizer"+'&token='+token
                    
                    eventorganizerjson=oauth.get(event_api_url).json()
                    
                    organizer_description=eventorganizerjson["organizer"]["description"]["text"]
                    organizer_name=eventorganizerjson["organizer"]["name"]
                    
                    

                    if event['is_free']==False:
                        event_api_url="https://www.eventbriteapi.com/v3/events/"+event['id']+"/?expand=ticket_availability"+'&token='+token
                    
                        eventcostjson=oauth.get(event_api_url).json()



                        has_available_tickets=eventcostjson["ticket_availability"]["has_available_tickets"]
                        minimum_ticket_price=eventcostjson["ticket_availability"]["minimum_ticket_price"]["major_value"]
                        maximum_ticket_price=eventcostjson["ticket_availability"]["maximum_ticket_price"]["major_value"]
                        ticket_update_kwargs={"has_available_tickets":has_available_tickets,"minimum_ticket_price":minimum_ticket_price,
                            "maximum_ticket_price":maximum_ticket_price,"organizer_name":organizer_name,"organizer_description":organizer_description}
                    else:
                       ticket_update_kwargs={"minimum_ticket_price":0.00,
                            "maximum_ticket_price":0.00,"organizer_name":organizer_name,"organizer_description":organizer_description} 

                      
                    
                    Event.objects.filter(external_id=event['id']).update(**ticket_update_kwargs)
                    Event.objects.filter(external_id=event['id']).update(**kwargs)
                
                
                elif Event.objects.filter(external_id=event['id']).exists():

                    Event.objects.filter(external_id=event['id']).update(**kwargs)
                else:    
                    e = Event.objects.create(external_id=event['id'], name=event['name']['text'])


                    
            # if hasattr(event['description'], 'html'):
            #     description=description+event['description']['html']
            # else:
            #     description=description+'NO HTML'
        
        pagecount=pagecount+1

    #return JsonResponse(oauth.get(api_url_with_token).json(),safe=False)
    #return JsonResponse(eventcostjson,safe=False)
    return JsonResponse(eventorganizerjson,safe=False)
    #return HttpResponse(oauth.get(api_url_with_token).json())
    #return HttpResponse(description)
    #return JsonResponse(event0json)
    
    
    # eventbrite = OAuth2Session(client_id)
    # authorization_url, state = eventbrite.authorization_url(authorization_base_url)
    # eventbrite = OAuth2Session(client_id, state=requests.session['oauth_state'])
    # token = eventbrite.fetch_token(token_url, client_secret=client_secret,authorization_response=request.url)

    
    # return jsonify(eventbrite.get('https://www.eventbriteapi.com/v3/events/search/').json())
    #return HttpResponse("Hello, world. You're at the events index.")