from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('fill_db/<int:pages>/<int:fill>/<int:start_page>/', views.fill_db, name='fill_db'),
    path('update/<slug:external_id>/', views.EventUpdate, name='update'),
]