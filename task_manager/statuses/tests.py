from django.test import TestCase
from task_manager.statuses.models import Statuses
from task_manager.users.models import Users
from django.urls import reverse


# Create your tests here.
# Class test functional model Status/ Класс тестирует функционал модели Status
class Statuses_Test(TestCase):
    def setUp(self):
        Users.objects.create(
            first_name='NoName',
            last_name='NoLastName',
            username='NoNameNoLastName',
            password='NoLastName123'
        )
        self.user = Users.objects.get(id=1)
        Statuses.objects.create(name='status1-work')
        Statuses.objects.create(name='status2-relax')
        Statuses.objects.create(name='status3-test')

    def test_access(self):
        '''Незалогинение пользователи получают редирект'''
        resp1 = self.client.get(reverse('status_create'))
        self.assertEqual(resp1.status_code, 302)
        resp2 = self.client.get(reverse('status_index'))
        self.assertEqual(resp2.status_code, 302)
        resp3 = self.client.get(reverse('status_update', kwargs={'pk': 1}))
        self.assertEqual(resp3.status_code, 302)
        resp4 = self.client.get(reverse('status_delete', kwargs={'pk': 1}))
        self.assertEqual(resp4.status_code, 302)
        '''Залогинимся'''
        self.client.force_login(self.user)
        resp1 = self.client.get(reverse('status_create'))
        self.assertEqual(resp1.status_code, 200)
        resp2 = self.client.get(reverse('status_index'))
        self.assertEqual(resp2.status_code, 200)
        resp3 = self.client.get(reverse('status_update', kwargs={'pk': 1}))
        self.assertEqual(resp3.status_code, 200)
        resp4 = self.client.get(reverse('status_delete', kwargs={'pk': 1}))
        self.assertEqual(resp4.status_code, 200)

    # Method tests status creation / Метод тестирует создание статус
    def test_CreateStatus(self):
        self.client.force_login(self.user)
        '''Добавим статус'''
        resp = self.client.post(reverse('status_create'), {'name': 'status4'})
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('status_index'))
        '''Проверяем добавлен ли новый статус'''
        resp = self.client.get(reverse('status_index'))
        self.assertTrue(len(resp.context['object_list']) == 4)

    def test_ListStatuses(self):
        self.client.force_login(self.user)
        resp = self.client.get(reverse('status_index'))
        self.assertTrue(len(resp.context['object_list']) == 3)

    # Method tests status update / Метод тестирует обновление статус
    def test_UpdateStatus(self):
        self.client.force_login(self.user)
        s1 = Statuses.objects.get(pk=1)
        resp = self.client.post(reverse('status_update', kwargs={'pk': 1}),
                                {'name': 'Updated Status'})
        self.assertEqual(resp.status_code, 302)
        s1.refresh_from_db()
        self.assertEqual(s1.name, 'Updated Status')

    # Method tests status delete / Метод тестирует удаление статус
    def test_DeleteStatus(self):
        self.client.force_login(self.user)
        self.assertEqual(Statuses.objects.count(), 3)
        resp = self.client.post(
            reverse('status_delete', kwargs={'pk': 3})
        )
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Statuses.objects.count(), 2)
        self.assertEqual(Statuses.objects.get(pk=1).name, 'status1-work')
        self.assertEqual(Statuses.objects.get(pk=2).name, 'status2-relax')
