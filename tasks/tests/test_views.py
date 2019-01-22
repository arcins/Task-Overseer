import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from ..models import Tasks
from ..serializers import TasksSerializer


# initialize the APIClient app
client = Client()

class GetAllTasksTest(TestCase):
    """ Test module for GET all tasks API """

    def setUp(self):
        Tasks.objects.create(
            title='task3', is_done=False, description='task3 test', date=timezone.now())
        Tasks.objects.create(
            title='task4', is_done=True, description='task4 test', date=timezone.now())
        Tasks.objects.create(
            title='task5', is_done=False, description='task5 test', date=timezone.now())
        Tasks.objects.create(
            title='task6', is_done=False, description='task6 test', date=timezone.now())

    def test_get_all_tasks(self):
        # get API response
        response = client.get(reverse('get_post_tasks'))
        # get data from db
        tasks = Tasks.objects.all()
        serializer = TasksSerializer(tasks, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSingleTaskTest(TestCase):
    """ Test module for GET single task API """

    def setUp(self):
        self.task1 = Tasks.objects.create(
            title='task1', is_done=False, description='task1 test', date=timezone.now())
        self.task2 = Tasks.objects.create(
            title='task2', is_done=False, description='task2 test', date=timezone.now())
        self.task3 = Tasks.objects.create(
            title='task3', is_done=False, description='task3 test', date=timezone.now())
        self.task4 = Tasks.objects.create(
            title='task4', is_done=False, description='task4 test', date=timezone.now())

    def test_get_valid_single_task(self):
        response = client.get(
            reverse('get_delete_update_task', kwargs={'pk': self.task3.pk}))
        task = Tasks.objects.get(pk=self.task3.pk)
        serializer = TasksSerializer(task)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_task(self):
        response = client.get(
            reverse('get_delete_update_task', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewTaskTest(TestCase):
    """ Test module for inserting a new task """

    def setUp(self):
        self.valid_payload = {
            'title': 'task1',
            'is_done': 'True',
            'description': 'task1 test',
            'date': '2012-11-01T04:16:13-04:00'
        }
        self.invalid_payload = {
            'title': '',
            'is_done': 'True',
            'description': 'task1 test',
            'date': '2012-11-01T04:16:13-04:00'
        }

    def test_create_valid_task(self):
        response = client.post(
            reverse('get_post_tasks'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_task(self):
        response = client.post(
            reverse('get_post_tasks'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class UpdateSingleTaskTest(TestCase):
    """ Test module for updating an existing task record """

    def setUp(self):
        self.task7 = Tasks.objects.create(
            title='task7', is_done=False, description='task7 test', date=timezone.now())
        self.task8 = Tasks.objects.create(
            title='task8', is_done=False, description='task8 test', date=timezone.now())
        self.valid_payload = {
            'title': 'task8',
            'is_done': 'True',
            'description': 'task8 test po zmianie',
            'date': '2012-11-01T04:16:13-04:00'
        }
        self.invalid_payload = {
            'title': '',
            'is_done': 'True',
            'description': 'task1 test po zmianie',
            'date': '2012-11-01T04:16:13-04:00'
        }

    def test_valid_update_task(self):
        response = client.put(
            reverse('get_delete_update_task', kwargs={'pk': self.task8.pk}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_update_task(self):
        response = client.put(
            reverse('get_delete_update_task', kwargs={'pk': self.task8.pk}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSingleTaskTest(TestCase):
    """ Test module for deleting an existing task record """

    def setUp(self):
        self.task9 = Tasks.objects.create(
            title='task9', is_done=False, description='task9 test', date=timezone.now())
        self.task10 = Tasks.objects.create(
            title='task10', is_done=False, description='task10 test', date=timezone.now())

    def test_valid_delete_puppy(self):
        response = client.delete(
            reverse('get_delete_update_task', kwargs={'pk': self.task10.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_puppy(self):
        response = client.delete(
            reverse('get_delete_update_task', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)