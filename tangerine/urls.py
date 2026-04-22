from django.urls import path
from . import views


urlpatterns = [
    path('',views.IndexView.as_view(),name='home'),
    path('contracts-list/',views.ContractsView.as_view(),name='contracts'),
    path('clients-view',views.AllClientsView.as_view(),name='clients'),

    path('client/<uuid:id>/',views.ClientView.as_view(),name='client'),

    path('add-client/',views.AddClientView.as_view(),name='add_client')
]