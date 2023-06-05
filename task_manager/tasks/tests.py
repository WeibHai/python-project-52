from django.test import TestCase
from django.urls import reverse
from task_manager.users.models import Users
from task_manager.statuses.models import Statuses
from task_manager.labels.models import Labels


# Create your tests here.
# Class test functional model Task
# Класс тестирует функционал модели Task
class Tasks_Test(TestCase):

    def setUp(self):
        Users.objects.create(
            first_name='NoName',
            last_name='NoLastName',
            username='NoNameNoLastName',
            password='NoLastName123'
        )
        self.user = Users.objects.get(id=1)

        Statuses.objects.create(name='status1')
        self.status = Statuses.objects.get(id=1)

        Labels.objects.create(name='label1')
        self.label = Labels.objects.get(id=1)

    url_tasks = [
        reverse('task_index'),
        reverse('task_create'),
        reverse('task_page', kwargs={'pk': 1}),
        reverse('task_update', kwargs={'pk': 1}),
        reverse('task_delete', kwargs={'pk': 1}),
    ]

    def test_access(self, urls=url_tasks):
        for u in urls:
            resp = self.client.get(u)
            self.assertEqual(resp.status_code, 302)
