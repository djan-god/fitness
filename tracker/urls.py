from django.urls import path
from . import views

app_name = 'tracker'

urlpatterns = [
    path('dashboard/', views.tracker_dashboard, name='dashboard'),
    path('history/', views.history_view, name='history'),
]
