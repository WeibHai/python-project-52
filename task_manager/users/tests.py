from django.test import TestCase
from .models import Users
from django.urls import reverse


# Create your tests here.
# Class test functional model User
# Класс тестирует функционал модели User
class Users_Test(TestCase):
    fixtures = ['users.json']

    @classmethod
    def setUpTestData(self, cls):
        Users.objects.create(
            first_name='Ivan',
            last_name='Ivanov',
            username='IvanIvanov',
            password='IvanIvanov123'
        )
        Users.objects.create(
            first_name='Anna',
            last_name='None',
            username='AnnaNone',
            password='AnnaNone123'
        )

    # Method tests user creation
    # Метод тестирует создание пользователя
    def test_SignUp(self):
        resp = self.client.get(reverse('user_create'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, template_name='users/users_create.html')

        resp = self.client.post(
            reverse('user_create'),
            {
                'first_name': 'Danil',
                'last_name': 'Danilovich',
                'username': 'DanilDanilovich',
                'password1': 'qqqqqqqqqqq',
                'password2': 'qqqqqqqqqqq',
            }
        )
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('login'))

        user = Users.objects.last()
        self.assertEqual(user.first_name, 'Danil')
        self.assertEqual(user.last_name, 'Danilovich')
        self.assertEqual(user.username, 'DanilDanilovich')

        '''Проверка наличия нового пользователя на сайте'''
        resp = self.client.get(reverse('user_index'))
        self.assertTrue(len(resp.context['object_list']) == 3)

    def test_ListUsers(self):
        resp = self.client.get(reverse('user_index'))
        self.assertTrue(len(resp.context['object_list']) == 2)

    # Method tests user update
    # Метод тестирует обновление пользователя
    def test_UpdateUser(self):
        user = Users.objects.get(id=1)
        '''Пробуем изменить данные без аутентификации'''
        resp = self.client.get(
            reverse('user_update', kwargs={'pk': user.id})
        )
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('login'))
        '''Изменяем данные первой учетной записи с пройденой аутентификацией'''
        self.client.force_login(user)
        resp = self.client.get(
            reverse('user_update', kwargs={'pk': user.id})
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, template_name='users/users_update.html')
        resp = self.client.post(
            reverse('user_update', kwargs={'pk': user.id}),
            {
                'first_name': 'NoName',
                'last_name': 'NoLastName',
                'username': 'NoNameNoLastName',
                'password1': '12345789sq',
                'password2': '12345789sq',
            }
        )
        self.assertEqual(resp.status_code, 302)
        user.refresh_from_db()
        self.assertEqual(user.first_name, 'NoName')

    # The method tests the deletion of a user
    # Метод тестирует удаление пользователя
    def test_DeleteUser(self):
        user = Users.objects.get(username='AnnaNone')
        '''Без аутентификации'''
        resp = self.client.get(reverse('user_delete', kwargs={'pk': user.id}))
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('login'))
        '''Зайдя в профиль'''
        self.client.force_login(user)
        resp = self.client.get(reverse('user_delete', kwargs={'pk': user.id}))
        self.assertEqual(resp.status_code, 200)

        resp = self.client.post(
            reverse('user_delete', kwargs={'pk': user.id})
        )
        self.assertRedirects(resp, reverse('user_index'))
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Users.objects.count(), 1)
