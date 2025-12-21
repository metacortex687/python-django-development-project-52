from django.test import TestCase
from django.contrib.auth.models import User

class TestUsersCRUD(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.password = '12345'

        cls.user1 = User.objects.create_user(username='user1', password=cls.password, first_name = 'F_U1', last_name = 'L_U1')
        cls.user2 = User.objects.create_user(username='user2', password=cls.password, first_name = 'F_U2', last_name = 'L_U2')

    def test_user_list(self):
        resp = self.client.get('/users/')
        self.assertEqual(resp.status_code,200)
        self.assertContains(resp, self.user1.username)
        self.assertContains(resp, self.user1.first_name)
        self.assertContains(resp, self.user1.last_name)

        self.assertContains(resp, self.user2.username)

    def test_user_create_get(self):
        resp = self.client.get('/users/create/')
        self.assertEqual(resp.status_code,200)


    def test_user_create_redirects_to_login(self):
        payload = {
            "first_name": "Alex",
            "last_name": "Test",
            "username": "new_user",
            "password1": "NewStrongPass_123",
            "password2": "NewStrongPass_123",
        }



        resp = self.client.post('/users/create/', payload)
        self.assertRedirects(resp, '/login/')
        self.assertTrue(User.objects.filter(username="new_user").exists())


    def test_user_update_get(self):
        resp = self.client.get('/users/1/update/')
        self.assertEqual(resp.status_code,200)


    def test_user_update_post(self):
        payload = {
            "username": "user1_change",
            "first_name": "",
            "last_name": "L1",
        }

        resp = self.client.post('/users/1/update/', payload)
        self.assertRedirects(resp, '/users/')
        self.assertTrue(User.objects.filter(username="user1_change").exists())


    def test_user_delete_get(self):
        resp = self.client.get('/users/1/delete/')
        self.assertEqual(resp.status_code,200)

    def test_user_delete_post(self):        
        self.assertTrue(User.objects.filter(pk=1).exists())
        resp = self.client.post('/users/1/delete/')
        self.assertRedirects(resp, '/users/')
        self.assertFalse(User.objects.filter(pk=1).exists())

    def test_login_get(self):
        resp = self.client.get('/login/')
        self.assertEqual(resp.status_code,200)

    def test_login_post(self):
        payload = {
            "username": "user1",
            "password": self.password,
        }
        resp = self.client.post('/login/', payload)
        self.assertRedirects(resp, '/')

        resp2 = self.client.get('/') 
        self.assertTrue(resp2.wsgi_request.user.is_authenticated)

    def test_logout_post(self):
        payload = {
            "username": "user1",
            "password": self.password,
        }
        resp = self.client.post('/login/', payload)
        self.assertRedirects(resp, '/')

        resp2 = self.client.get('/') 
        self.assertTrue(resp2.wsgi_request.user.is_authenticated)

        resp = self.client.post('/logout/', payload)
        self.assertRedirects(resp, '/')

        resp2 = self.client.get('/') 
        self.assertFalse(resp2.wsgi_request.user.is_authenticated)