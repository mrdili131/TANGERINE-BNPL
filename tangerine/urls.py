from django.urls import path
from . import views


urlpatterns = [
    path('',views.IndexView.as_view(),name='home'),
    path('contracts-list/',views.ContractsView.as_view(),name='contracts'),
    path('clients-view',views.AllClientsView.as_view(),name='clients'),

    path('client/<uuid:id>/',views.ClientView.as_view(),name='client'),
    path('edit-client/<uuid:client_id>/',views.EditClientView.as_view(),name='edit_client'),

    path('add-client/',views.AddClientView.as_view(),name='add_client'),

    # api like
    path('get-numbers/<uuid:client_id>/',views.get_numbers,name='get_numbers'),

    path('delete-number/<int:id>/',views.delete_number,name='delete_number'),

    path('add-number/',views.add_number,name='add_number')
]