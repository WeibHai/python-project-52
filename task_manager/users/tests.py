from django.test import TestCase
from .models import Users
from django.urls import reverse

# Create your tests here.
class CRUD_Users_Test(TestCase):

    @classmethod
    def setUpTestData(cls):
        Users.objects.create(
            first_name='Ivan',
            last_name='Grozniy',
            username='IvGroz',
            email='ivan@google.ru',
            password='Iv123'
        )
        Users.objects.create(
            first_name='Mariya',
            last_name='Petrova',
            username='Masha003',
            email='masha@mail.ru',
            password='quni'
        )

    # CREATE - Регистрация нового пользователя
    def test_SignUp(self):
        resp = self.client.get(reverse('user_create'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, template_name='users/users_create.html')

        resp = self.client.post(
            reverse('user_create'),
            {
                'first_name': 'Alexey',
                'last_name': 'Navalny',
                'username': 'FBK',
                'password1': 'iloveputin',
                'password2': 'iloveputin',
            }
        )
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('login'))

        user = Users.objects.last()
        self.assertEqual(user.first_name, 'Alexey')
        self.assertEqual(user.last_name, 'Navalny')
        self.assertEqual(user.username, 'FBK')

        '''Проверка наличия нового пользователя на сайте'''
        resp = self.client.get(reverse('user_index'))
        self.assertTrue(len(resp.context['object_list']) == 3)

    # READ - вывод списка всех пользователей
    def test_ListUsers(self):
        resp = self.client.get(reverse('user_index'))
        self.assertTrue(len(resp.context['object_list']) == 2)

    # UPDATE - обновленние данных пользователя
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
                'first_name': 'Petya',
                'last_name': 'Piter',
                'username': 'Petr1',
                'password1': 'lovePiter',
                'password2': 'lovePiter',
            }
        )
        self.assertEqual(resp.status_code, 302)
        user.refresh_from_db()
        self.assertEqual(user.first_name, 'Petya')

    # DELETE - удаления пользователя
    def test_DeleteUser(self):
        user = Users.objects.get(username='Masha003')
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