from django.test import TestCase
from .models import Status, Task, Label
from django.contrib.auth import get_user_model

User = get_user_model()


class TestTuskCRUD(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.status1 = Status.objects.create(name="status1")
        cls.status2 = Status.objects.create(name="status2")

        cls.password = "StrongPass_123"
        cls.user1 = User.objects.create_user(
            username="user1", password=cls.password
        )
        cls.user2 = User.objects.create_user(
            username="user2", password=cls.password
        )

        cls.task1 = Task.objects.create(
            name="task1",
            describe="describe1",
            status=cls.status1,
            author=cls.user1,
            executor=cls.user2,
        )
        cls.task2 = Task.objects.create(
            name="task2",
            describe="describe2",
            status=cls.status2,
            author=cls.user2,
            executor=cls.user1,
        )

    def test_task_list(self):
        resp = self.client.get("/tasks/")
        self.assertRedirects(resp, "/login/?next=/tasks/")

        self.client.login(username=self.user1.username, password=self.password)

        resp = self.client.get("/tasks/")
        self.assertEqual(resp.status_code, 200)

        self.assertContains(resp, self.task1.name)
        self.assertContains(resp, self.task2.name)

    def test_task_create_get(self):
        resp = self.client.get("/tasks/create/")
        self.assertRedirects(resp, "/login/?next=/tasks/create/")

        self.client.login(username=self.user1.username, password=self.password)

        resp = self.client.get("/tasks/")
        self.assertEqual(resp.status_code, 200)

    def test_task_create_post(self):
        payload = {
            "name": "new_task",
            "describe": "new_describe",
            "status": self.status1.pk,
            "executor": self.user2.pk,
        }

        resp = self.client.post("/tasks/create/", payload)

        self.assertRedirects(resp, "/login/?next=/tasks/create/")
        self.assertFalse(Task.objects.filter(name="new_task").exists())

        self.client.login(username=self.user1.username, password=self.password)

        resp = self.client.post("/tasks/create/", payload)
        self.assertRedirects(resp, "/tasks/")

        task = Task.objects.get(name="new_task")
        self.assertEqual(task.describe, "new_describe")
        self.assertEqual(task.status, self.status1)
        self.assertEqual(task.executor, self.user2)
        self.assertEqual(task.author, self.user1)

    def test_task_update_get(self):
        resp = self.client.get("/tasks/1/update/")

        self.assertRedirects(resp, "/login/?next=/tasks/1/update/")

        self.client.login(username=self.user1.username, password=self.password)

        resp = self.client.get("/tasks/1/update/")
        self.assertEqual(resp.status_code, 200)

    def test_task_update_post(self):
        payload = {
            "name": "rename_task",
            "describe": "rename_describe",
            "status": self.status2.pk,
            "executor": self.user1.pk,
        }

        resp = self.client.post("/tasks/1/update/", payload)

        self.assertRedirects(resp, "/login/?next=/tasks/1/update/")
        self.assertFalse(Task.objects.filter(name="rename_status").exists())

        task = Task.objects.get(pk=1)
        self.assertEqual(task.name, "task1")
        self.assertEqual(task.describe, "describe1")
        self.assertEqual(task.status, self.status1)
        self.assertEqual(task.executor, self.user2)
        self.assertEqual(task.author, self.user1)

        self.client.login(username=self.user2.username, password=self.password)

        resp = self.client.post("/tasks/1/update/", payload)
        self.assertRedirects(resp, "/tasks/1/")

        task.refresh_from_db()
        self.assertEqual(task.name, "rename_task")
        self.assertEqual(task.describe, "rename_describe")
        self.assertEqual(task.status, self.status2)
        self.assertEqual(task.executor, self.user1)
        self.assertEqual(
            task.author, self.user1
        )  # на сайте образце после обновления автор не меняется

    def test_task_delete_get(self):
        resp = self.client.get("/tasks/1/delete/")

        self.assertRedirects(resp, "/login/?next=/tasks/1/delete/")

        self.client.login(username=self.user1.username, password=self.password)

        resp = self.client.get("/tasks/1/delete/")
        self.assertEqual(resp.status_code, 200)

    def test_task_delete_post(self):
        resp = self.client.post("/tasks/1/delete/")

        self.assertRedirects(resp, "/login/?next=/tasks/1/delete/")
        self.assertTrue(Task.objects.filter(name="task1").exists())

        self.client.login(username=self.user1.username, password=self.password)

        resp = self.client.post("/tasks/1/delete/")
        self.assertRedirects(resp, "/tasks/")

        self.assertFalse(Task.objects.filter(name="task1").exists())

    def test_reverse_tasks_for_status(self):
        self.status1.task_set.all()
        self.assertIn(self.task1, self.status1.task_set.all())
        self.assertNotIn(self.task2, self.status1.task_set.all())

    def test_filter_task(self):
        self.client.login(username=self.user1.username, password=self.password)

        resp = self.client.get("/tasks/", {"status": "", "executor": ""})

        self.assertContains(resp, self.task1.name)
        self.assertContains(resp, self.task2.name)

        resp = self.client.get("/tasks/", {"self_tasks": "on"})
        self.assertContains(resp, self.task1.name)
        self.assertNotContains(resp, self.task2.name)

        resp = self.client.get("/tasks/", {"status": 2})
        self.assertNotContains(resp, self.task1.name)
        self.assertContains(resp, self.task2.name)

    def test_filter_task_for_label(self):
        self.client.login(username=self.user1.username, password=self.password)

        label1 = Label.objects.create(name="label1")
        self.task1.labels.add(label1)

        resp = self.client.get("/tasks/", {"label": label1.id})

        self.assertContains(resp, self.task1.name)
        self.assertNotContains(resp, self.task2.name)

        label2 = Label.objects.create(name="label2")
        self.task1.labels.add(label2)
        self.task2.labels.add(label2)

        resp = self.client.get("/tasks/", {"label": label2.id})

        self.assertContains(resp, self.task1.name)
        self.assertContains(resp, self.task2.name)

        label3 = Label.objects.create(name="label3")
        resp = self.client.get("/tasks/", {"label": label3.id})
        self.assertNotContains(resp, self.task1.name)
        self.assertNotContains(resp, self.task2.name)
