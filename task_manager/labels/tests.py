from django.test import TestCase
from .models import Label
from django.contrib.auth import get_user_model

User = get_user_model()


class TestLabelCRUD(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.label1 = Label.objects.create(name="label1")
        cls.label2 = Label.objects.create(name="label2")

        cls.password = "StrongPass_123"
        cls.user = User.objects.create_user(
            username="user1", password=cls.password
        )

    def test_label_list(self):
        resp = self.client.get("/labels/")
        self.assertRedirects(resp, "/login/?next=/labels/")

        self.client.login(username=self.user.username, password=self.password)

        resp = self.client.get("/labels/")
        self.assertEqual(resp.status_code, 200)

        self.assertContains(resp, self.label1.name)
        self.assertContains(resp, self.label2.name)

    def test_label_create_get(self):
        resp = self.client.get("/labels/create/")
        self.assertRedirects(resp, "/login/?next=/labels/create/")

        self.client.login(username=self.user.username, password=self.password)

        resp = self.client.get("/labels/")
        self.assertEqual(resp.status_code, 200)

    def test_label_create_post(self):
        payload = {
            "name": "new_label",
        }

        resp = self.client.post("/labels/create/", payload)

        self.assertRedirects(resp, "/login/?next=/labels/create/")
        self.assertFalse(Label.objects.filter(name="new_label").exists())

        self.client.login(username=self.user.username, password=self.password)

        resp = self.client.post("/labels/create/", payload)
        self.assertRedirects(resp, "/labels/")
        self.assertTrue(Label.objects.filter(name="new_label").exists())

    def test_label_update_get(self):
        resp = self.client.get("/labels/1/update/")

        self.assertRedirects(resp, "/login/?next=/labels/1/update/")

        self.client.login(username=self.user.username, password=self.password)

        resp = self.client.get("/labels/1/update/")
        self.assertEqual(resp.status_code, 200)

    def test_label_update_post(self):
        payload = {
            "name": "rename_label",
        }

        resp = self.client.post("/labels/1/update/", payload)

        self.assertRedirects(resp, "/login/?next=/labels/1/update/")
        self.assertFalse(Label.objects.filter(name="rename_label").exists())

        self.client.login(username=self.user.username, password=self.password)

        resp = self.client.post("/labels/1/update/", payload)
        self.assertRedirects(resp, "/labels/")

        self.assertTrue(Label.objects.filter(name="rename_label").exists())

        self.label1.refresh_from_db()
        self.assertEqual(self.label1.name, "rename_label")

    def test_label_delete_get(self):
        resp = self.client.get("/labels/1/delete/")

        self.assertRedirects(resp, "/login/?next=/labels/1/delete/")

        self.client.login(username=self.user.username, password=self.password)

        resp = self.client.get("/labels/1/delete/")
        self.assertEqual(resp.status_code, 200)

    def test_label_delete_post(self):
        resp = self.client.post("/labels/1/delete/")

        self.assertRedirects(resp, "/login/?next=/labels/1/delete/")
        self.assertTrue(Label.objects.filter(name="label1").exists())

        self.client.login(username=self.user.username, password=self.password)

        resp = self.client.post("/labels/1/delete/")
        self.assertRedirects(resp, "/labels/")

        self.assertFalse(Label.objects.filter(name="label1").exists())
