from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from .models import Labels
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from django_filters.views import FilterView
from django.utils.translation import gettext_lazy as _
from django.shortcuts import render

# Create your views here.
# Класс который содержит все общие атрибуты классов CRUD
class LabelsMixin(LoginRequiredMixin, SuccessMessageMixin):
    model = Labels
    extra_context = {'title': _('New Labels'), 'button': _('Create')}
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('label_index')
    fields = ['name']


class LabelsListView(LabelsMixin, FilterView):
    context_object_name = 'labels'
    extra_context = {'title': _('Labels')}
    template_name = 'labels/labels_list.html'


class LabelsCreateView(LabelsMixin, CreateView):
    template_name = 'labels/labels_create.html'
    success_message = _("Label created successfully")

    # Добавляем имя автора в поле author, которое не отображается в форме
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class LabelsUpdateView(LabelsMixin, UpdateView):
    template_name = 'labels/labels_update.html'
    extra_context = {'title': _('Update label'), 'button': _('Change')}
    success_message = _('Label successfully changed')


class LabelsDeleteView(LabelsMixin, DeleteView):
    template_name = 'labels/labels_delete.html'
    success_message = _('Label successfully deleted')

    def post(self, request, *args, **kwargs):
        try:
            self.delete(request, *args, **kwargs)
            messages.success(
                self.request,
                _('Label successfully deleted')
            )
            return redirect(reverse_lazy('label_index'))
        except ProtectedError:
            messages.error(
                self.request,
                _("Error! Can't delete, label in use")
            )
            return redirect(reverse_lazy('label_index'))
