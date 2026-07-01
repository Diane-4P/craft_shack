from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
    path('terms_and_conditions/', views.terms_and_conditions, name='terms_and_conditions'),
    path('returns_and_refunds/', views.returns_and_refunds, name='returns_and_refunds'),
    path('shipping_policy/', views.shipping_policy, name='shipping_policy'),
]
