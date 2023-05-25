from .models import Users
from .forms import UsersForm
from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.utils import timezone

# Create your views here.
class UsersListView(ListView):
    model = Users
    template_name="users.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class UsersCreateView(CreateView):
    form_class = UsersForm
    template_name = 'users/users_create.html'
    success_url = reverse_lazy('login')


class RulesMixin:

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


class UsersUpdateView(RulesMixin, UpdateView):
    model = Users
    fields = ['first_name', 'last_name', 'username']
    template_name="users/users_update.html"
    success_url = reverse_lazy('user_index')


class UsersDeleteView(RulesMixin, DeleteView):
    model = Users
    template_name = "users/users_delete.html"
    success_url = reverse_lazy('user_index')
