from django.views.generic import TemplateView
from django.utils.translation import gettext_lazy as _
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView


class IndexView(SuccessMessageMixin, TemplateView):
    template_name = "index.html"


class LogIn(SuccessMessageMixin, LoginView):
    template_name = "login.html"
    success_message = 'Successfully login'


class LogOut(LogoutView):
    success_message = _('Successfully logout')

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.add_message(request, messages.INFO, self.success_message)
        return response
