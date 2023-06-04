from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.shortcuts import render, redirect
from django_filters.views import FilterView
from django.urls import reverse_lazy
from django.contrib import messages
from .filters import TaskFilter
from .models import Tasks


# Create your views here.
# Mixin classes with common attributes / Класс-примесь с общими атрибутами
class TasksMixin(SuccessMessageMixin, LoginRequiredMixin):
    model = Tasks
    extra_context = {'title': _('New Tasks'), 'button': _('Create')}
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('task_index')
    fields = ['name', 'description', 'status', 'executor', 'labels']


# The class displays a list of model instances / Класс отображает список экземпляров модели
class TasksListView(TasksMixin, FilterView):
    context_object_name = 'tasks'
    extra_context = {'title': _('Tasks')}
    template_name = 'tasks/tasks_list.html'
    filterset_class = TaskFilter

# The class creates an instance of the model / Класс создает экземпляр модели
class TasksCreateView(TasksMixin, CreateView):
    template_name = 'tasks/tasks_create.html'
    success_message = _("Task created successfully")

    # Добавляем имя автора в поле author, которое не отображается в форме
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# The class displays detailed information about the model / Класс отображает подобробную иформацию о моделе
class TaskView(TasksMixin, DetailView):
    context_object_name = 'task'
    extra_context = {'title': _('Show task')}
    template_name = 'tasks/tasks_page.html'

# The class changes information about the model instance / Класс изменяет информацию о экземпляре моделе
class TasksUpdateView(TasksMixin, UpdateView):
    template_name = 'tasks/tasks_update.html'
    extra_context = {'title': _('Update task'), 'button': _('Change')}
    success_message = _('Task changed')

# The class deletes the model instance / Класс удаляет экземпляр модели
class TasksDeleteView(TasksMixin, DeleteView):
    template_name = 'tasks/tasks_delete.html'
    success_message = _('Task deleted')

    def has_permission(self) -> bool:
        return self.get_object().author.pk == self.request.user.pk

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(
                self.request,
                _("Error! You are not authenticated")
            )
            return self.handle_no_permission()

        elif not self.has_permission():
            messages.error(
                request,
                _("Error! You can't delete this task. Only author")
            )
            return redirect('task_index')
        return super().dispatch(request, *args, **kwargs)
