from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.shortcuts import redirect
from django.db.models import ProtectedError
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Statuses


# Create your views here.
# Mixin classes with common attributes
# Класс-примесь с общими атрибутами
class StatusMixin(SuccessMessageMixin, LoginRequiredMixin):
    model = Statuses
    success_url = reverse_lazy('status_index')
    login_url = reverse_lazy('login')
    fields = ['name']


# The class displays a list of model instances
# Класс отображает список экземпляров модели
class StatusesListView(StatusMixin, ListView):
    template_name = "statuses_list.html"


# The class creates an instance of the model
# Класс создает экземпляр модели
class StatusesCreateView(StatusMixin, CreateView):
    template_name = 'statuses/statuses_create.html'
    success_message = _('Status created')


# The class changes information about the model instance
# Класс изменяет информацию о экземпляре моделе
class StatusesUpdateView(StatusMixin, UpdateView):
    template_name = 'statuses/statuses_update.html'
    success_message = _('Status changed')


# The class deletes the model instance
# Класс удаляет экземпляр модели
class StatusesDeleteView(StatusMixin, DeleteView):
    template_name = 'statuses/statuses_delete.html'
    success_message = _('Status deleted')

    def post(self, request, *args, **kwargs):
        try:
            self.delete(request, *args, **kwargs)
            return redirect(reverse_lazy('status_index'))
        except ProtectedError:
            messages.error(self.request,
                           _("Error! Can't delete, status in use"))
            return redirect(reverse_lazy('status_index'))
