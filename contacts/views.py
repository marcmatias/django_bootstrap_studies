from django.shortcuts import render
from django.http import HttpResponse
from .models import Contact

def index(request):
    contacts_list = Contact.objects
    context = {'contacts_list': contacts_list}
    return render(request, 'index.html', context)