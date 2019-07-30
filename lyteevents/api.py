from rest_framework import routers
from djangolyteevents import views as myapp_views
from django.urls import include, path

router = routers.DefaultRouter()
router.register(r'events', myapp_views.EventList)
#router.register(r'events/update/<int:external_id>/', myapp_views.EventUpdate)

# urlpatterns = [
#     path('update/<int:external_id>/', myapp_views.EventUpdate),
# ]
# urlpatterns += router.urls
