from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy

# from django.utils import timezone
# from django.views.generic.edit import CreateView
# from django.views.generic.list import ListView
# from django.views.generic.edit import DeleteView
# from django.views.generic.edit import UpdateView
# from django.urls import reverse_lazy, reverse\
# from django.shortcuts import get_object_or_404, render, redirect
# from django.views import View
# from task_manager.models import User
# from task_manager.forms import AddUserForm
# from django.contrib.auth.forms import AuthenticationForm


class IndexView(TemplateView):
    template_name="index.html"


class SignUp(LoginView):
    template_name="login.html"


class LogOut(LogoutView):

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        return response

