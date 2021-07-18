from django.shortcuts import render
from django.http import HttpResponse
from .models import Contact
from django.views.generic import ListView
from django.db.models import Q


def index(request):
    contacts_list = Contact.objects
    context = {'contacts_list': contacts_list}
    return render(request, 'index.html', context)


class ContactListView(ListView):
    model = Contact
    template_name = 'contact_list.html'
    paginate_by = 10
    ordering = ['-first_name']

    def get_queryset(self):
        queryset = super(ContactListView, self).get_queryset()
        data = self.request.GET

        search = data.get('search')
        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(email__icontains=search) |
                Q(birthday__icontains=search)
            )
        return queryset

    def get_ordering(self):
        ordering = self.request.GET.get('ordering', 'first_name')

        poped = [self.ordering.pop()]
        if ordering in poped:
            self.ordering.append('-'+ordering)
        elif '-'+ordering in poped:
            self.ordering.append(ordering)
        else:
            self.ordering.append(ordering)

        return self.ordering

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['name'] = 'Contatos'
        context['fields'] = [
            {'f_normalized': f.name.capitalize().replace('_', ' '),
             'f_name': f.name}
            for f
            in self.model._meta.get_fields()
        ][1:]

        return context
