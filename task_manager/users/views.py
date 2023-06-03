from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic.list import ListView
from django.urls import reverse_lazy, reverse
from django.shortcuts import render
from django.utils import timezone
from django.views import View
from .forms import UsersForm
from .models import Users


# Create your views here.
# The class displays a list of model instances / Класс отображает список экземпляров модели
class UsersListView(ListView):
    model = Users
    template_name="users/users_list.html.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

# The class creates an instance of the model / Класс создает экземпляр модели
class UsersCreateView(CreateView):
    template_name = 'users/users_create.html'
    success_url = reverse_lazy('login')
    form_class = UsersForm
    
# Mixin classes for classes UsersUpdateView, UsersDeleteView / Классы-примесь для классов UsersUpdateView, UsersDeleteView
class RulesMixin:
    model = Users
    success_url = reverse_lazy('user_index')
    fields = ['first_name', 'last_name', 'username']

    def has_permission(self) -> bool:
        return self.get_object().pk == self.request.user.pk

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # messages.error(
            #     request,
            #     messages.error(self.request, _('You are not authorized!'))
            # )
            return redirect('login')

        elif not self.has_permission():
            # messages.error(
            #     request,
            #     messages.error(self.request, _("You have't permission!"))
            # )
            return redirect('user_index')
        return super().dispatch(request, *args, **kwargs)

# The class changes information about the model instance / Класс изменяет информацию о экземпляре моделе
class UsersUpdateView(RulesMixin, UpdateView):
    template_name="users/users_update.html"

# The class deletes the model instance / Класс удаляет экземпляр модели
class UsersDeleteView(RulesMixin, DeleteView):
    template_name = "users/users_delete.html"
