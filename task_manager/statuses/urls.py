"""
URL configuration for task_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from .views import StatusesListView as ListView
from .views import StatusesUpdateView as UpdateView
from .views import StatusesCreateView as CreateView
from .views import StatusesDeleteView as DeleteView
from django.urls import path


urlpatterns = [
    path('', ListView.as_view(), name='status_index'),
    path('create/', CreateView.as_view(), name='status_create'),
    path('<int:pk>/update/', UpdateView.as_view(), name='status_update'),
    path('<int:pk>/delete/', DeleteView.as_view(), name='status_delete'),
]
