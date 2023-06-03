from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.db.models import ProtectedError
from django_filters.views import FilterView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import render
from .models import Labels

# Create your views here.
# Mixin classes with common attributes / Класс-примесь с общими атрибутами
class LabelsMixin(LoginRequiredMixin, SuccessMessageMixin):
    model = Labels
    extra_context = {'title': _('New Labels'), 'button': _('Create')}
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('label_index')
    fields = ['name']

# The class displays a list of model instances / Класс отображает список экземпляров модели
class LabelsListView(LabelsMixin, FilterView):
    context_object_name = 'labels'
    extra_context = {'title': _('Labels')}
    template_name = 'labels/labels_list.html'

# The class creates an instance of the model / Класс создает экземпляр модели
class LabelsCreateView(LabelsMixin, CreateView):
    template_name = 'labels/labels_create.html'
    success_message = _("Label created successfully")

    # Добавляем имя автора в поле author, которое не отображается в форме
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# The class changes information about the model instance / Класс изменяет информацию о экземпляре моделе
class LabelsUpdateView(LabelsMixin, UpdateView):
    template_name = 'labels/labels_update.html'
    extra_context = {'title': _('Update label'), 'button': _('Change')}
    success_message = _('Label successfully changed')

# The class deletes the model instance / Класс удаляет экземпляр модели
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
