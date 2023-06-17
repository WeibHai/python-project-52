from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.shortcuts import redirect
from django.db.models import ProtectedError
from django.views.generic.list import ListView
from django.http import HttpResponseRedirect
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils import timezone
from .forms import UsersForm
from .models import Users


# Create your views here.
# The class displays a list of model instances
# Класс отображает список экземпляров модели
class UsersListView(SuccessMessageMixin, ListView):
    model = Users
    template_name = "users/users_list.html.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


# The class creates an instance of the model
# Класс создает экземпляр модели
class UsersCreateView(SuccessMessageMixin, CreateView):
    template_name = 'users/users_create.html'
    success_message = _('User created')
    success_url = reverse_lazy('login')
    form_class = UsersForm


# Mixin classes for classes UsersUpdateView, UsersDeleteView
# Класс-примесь для классов UsersUpdateView, UsersDeleteView
class UsersMixin:

    def has_permission(self) -> bool:
        return self.get_object().pk == self.request.user.pk

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(
                request,
                messages.error(self.request, _('You are not authorized!'))
            )
            return redirect('login')

        elif not self.has_permission():
            messages.error(
                request,
                messages.error(self.request, _("You have't permission!"))
            )
            return redirect('user_index')
        return super().dispatch(request, *args, **kwargs)


# The class changes information about the model instance
# Класс изменяет информацию о экземпляре моделе
class UsersUpdateView(SuccessMessageMixin, UsersMixin, UpdateView):
    model = Users
    form_class = UsersForm
    success_url = reverse_lazy('user_index')
    success_message = _('User changed')
    template_name = "users/users_update.html"


# The class deletes the model instance
# Класс удаляет экземпляр модели
class UsersDeleteView(SuccessMessageMixin, UsersMixin, DeleteView):
    model = Users
    success_url = reverse_lazy('user_index')
    success_message = _('User successfully deleted')
    error_message = _("Cannot delete a user because he is being used")
    template_name = "users/users_delete.html"

    def form_valid(self, form):
        success_url = self.get_success_url()
        try:
            self.object.delete()
        except ProtectedError:
            messages.success(
                self.request, (self.error_message),
            )
        else:
            messages.success(
                self.request, (self.success_message),
            )
        return HttpResponseRedirect(success_url)
