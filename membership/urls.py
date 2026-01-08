# membership/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.membership_dashboard, name='membership_dashboard'),
    path('create/', views.create_membership, name='create_membership'),
    path('pay/', views.process_payment, name='process_payment'),
    path('history/', views.payment_history, name='payment_history'),
]
