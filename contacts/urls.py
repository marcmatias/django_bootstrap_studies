from django.urls import path
from . import views

app_name = "contacts"

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/<int:num>', views.index, name='index'),
    path('contact/', views.ContactListView.as_view(), name='contact_list'),
    path('contact/delete', views.ContactDeleteView.as_view(), name='contact_delete'),
]