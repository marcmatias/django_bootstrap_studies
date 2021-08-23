from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from .models import Contact
from django.views.generic import ListView, DeleteView
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
from django.http import Http404 
from django.utils.translation import gettext as _

def index(request):
    contacts_list = Contact.objects
    context = {'contacts_list': contacts_list}
    return render(request, 'index.html', context)


class ContactListView(ListView):
    model = Contact
    template_name = 'contact_list.html'
    paginate_by = 10
    page_kwarg = 'pag'
    ordering = ['first_name']
    success_url = reverse_lazy('contacts:contact_list')
    
    def paginate_queryset(self, queryset, page_size):
        paginator = self.get_paginator(
            queryset, page_size, orphans=self.get_paginate_orphans(),
            allow_empty_first_page=self.get_allow_empty())
        page_kwarg = self.page_kwarg
        page = self.kwargs.get(page_kwarg) or self.request.GET.get(page_kwarg) or 1
        try:
            page_number = int(page)
        except ValueError:
            if page == 'last':
                page_number = paginator.num_pages
            else:
                raise Http404(_('Page is not “last”, nor can it be converted to an int.'))
        try:
            page = paginator.page(page_number)
        except InvalidPage as e:
            page = paginator.page(paginator.num_pages)
        return (paginator, page, page.object_list, page.has_other_pages())
            # raise Http404(_('Invalid page (%(page_number)s): %(message)s') % {
            #     'page_number': page_number,
            #     'message': str(e)
            # })

    def get_queryset(self):
        queryset = super(ContactListView, self).get_queryset()
        data = self.request.GET

        search = data.get('pesq')
        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(email__icontains=search) |
                Q(birthday__icontains=search)
            )

        return queryset

    def get_paginate_by(self, request):
        return self.request.GET.get('p_by', self.paginate_by)

    def get_ordering(self):
        col = self.request.GET.get('col', 'first_name')
        ord = self.request.GET.get('ord', None)
        if(ord and ord == ">"):
            return "-"+col

        return col

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['name'] = 'Contatos'
        context['fields'] = [
            {'f_normalized': f.name.capitalize().replace('_', ' '),
             'f_name': f.name}
            for f
            in self.model._meta.get_fields()
        ][1:]

        # Pagination options
        context["paginate_opts"] = ["10", "25", "75", "100"]
        context["p_by"] = self.get_paginate_by(self.request)

        # Column ordering
        ord = self.request.GET.get('ord', None)
        context['ord'] = "<" if ord and ord == ">" else ">"

        return context


class ContactDeleteView(DeleteView):
    model = Contact
    items_to_delete = []

    def post(self, request):
        items_to_delete = [el[10:]
                           for el in request.POST if el.startswith("selection_")]
        Contact.objects.filter(pk__in=items_to_delete).delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
