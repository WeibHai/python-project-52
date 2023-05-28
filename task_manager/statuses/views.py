from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.urls import reverse_lazy
from django.utils import timezone
from django.shortcuts import render, redirect
from .models import Statuses

# Create your views here.
class StatusMixin(LoginRequiredMixin, SuccessMessageMixin):
    model = Statuses
    login_url = reverse_lazy('login')
    fields = ['name']


class StatusesListView(ListView):
    model = Statuses
    template_name="statuses_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

class StatusesCreateView(StatusMixin, CreateView):
    template_name = 'statuses/statuses_create.html'
    success_url = reverse_lazy('status_index')
    

class StatusesUpdateView(StatusMixin, UpdateView):
    template_name = 'statuses/statuses_update.html'
    success_url = reverse_lazy('status_index')

class StatusesDeleteView(StatusMixin, DeleteView):
    template_name = 'statuses/statuses_delete.html'
    success_url = reverse_lazy('status_index')

    def post(self, request, *args, **kwargs):
        try:
            self.delete(request, *args, **kwargs)
            return redirect(reverse_lazy('status_index'))
        except ProtectedError:
            #messages.error(
            #    self.request,
            #    _("Error! Can't delete, status in use")
            #)
            return redirect(reverse_lazy('home_statuses'))