from rest_framework import routers
from djangolyteevents import views as myapp_views

router = routers.DefaultRouter()
router.register(r'events', myapp_views.EventList)