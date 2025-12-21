from django.test import TestCase
from .models import Status
from django.contrib.auth.models import User

class TestUsersCRUD(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.status1 = Status.objects.create(name='status1')
        cls.status2  = Status.objects.create(name='status2')

        cls.password = "StrongPass_123"
        cls.user = User.objects.create_user(username="user1", password=cls.password)




    def test_status_list(self):
        resp = self.client.get('/statuses/')
        self.assertRedirects(resp, '/login/?next=/statuses/')

        self.client.login(username=self.user.username, password=self.password)

        resp = self.client.get('/statuses/')
        self.assertEqual(resp.status_code,200)

        self.assertContains(resp, self.status1.name)
        self.assertContains(resp, self.status2.name)


    def test_status_create_get(self):
        resp = self.client.get('/statuses/create/')
        self.assertRedirects(resp, '/login/?next=/statuses/create/')

        self.client.login(username=self.user.username, password=self.password)

        resp = self.client.get('/statuses/')
        self.assertEqual(resp.status_code,200)



    def test_status_create_post(self):
        payload = {
            "name": "new_status",
        }

        resp = self.client.post('/statuses/create/', payload)

        self.assertRedirects(resp, '/login/?next=/statuses/create/')
        self.assertFalse(Status.objects.filter(name="new_status").exists())

        self.client.login(username=self.user.username, password=self.password)

        resp = self.client.post('/statuses/create/', payload)
        self.assertRedirects(resp, '/statuses/')
        self.assertTrue(Status.objects.filter(name="new_status").exists())

    def test_status_update_get(self):
        resp = self.client.get('/statuses/1/update/')

        self.assertRedirects(resp, '/login/?next=/statuses/1/update/')

        self.client.login(username=self.user.username, password=self.password)

        resp = self.client.get('/statuses/1/update/')
        self.assertEqual(resp.status_code,200)    


    def test_status_update_post(self):

        payload = {
            "name": "rename_status",
        }

        resp = self.client.post('/statuses/1/update/',payload)

        self.assertRedirects(resp, '/login/?next=/statuses/1/update/')
        self.assertFalse(Status.objects.filter(name="rename_status").exists())


        self.client.login(username=self.user.username, password=self.password)

        resp = self.client.post('/statuses/1/update/',payload)
        self.assertRedirects(resp, '/statuses/')  

        self.assertTrue(Status.objects.filter(name="rename_status").exists())

        self.status1.refresh_from_db()
        self.assertEqual(self.status1.name,'rename_status')


    def test_status_delete_get(self):
        resp = self.client.get('/statuses/1/delete/')

        self.assertRedirects(resp, '/login/?next=/statuses/1/delete/')

        self.client.login(username=self.user.username, password=self.password)

        resp = self.client.get('/statuses/1/delete/')
        self.assertEqual(resp.status_code,200)    


    def test_status_delete_post(self):

        resp = self.client.post('/statuses/1/delete/')

        self.assertRedirects(resp, '/login/?next=/statuses/1/delete/')
        self.assertTrue(Status.objects.filter(name="status1").exists())


        self.client.login(username=self.user.username, password=self.password)

        resp = self.client.post('/statuses/1/delete/')
        self.assertRedirects(resp, '/statuses/')  

        self.assertFalse(Status.objects.filter(name="rename_status").exists())
