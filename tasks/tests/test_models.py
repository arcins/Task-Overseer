from django.test import TestCase
from django.utils import timezone
from ..models import Tasks


class TaskTest(TestCase):
    """ Test module for Puppy model """

    def setUp(self):
        Tasks.objects.create(
            title='task1', is_done=False, description='task1 test', date = timezone.now())
        Tasks.objects.create(
            title='task2', is_done=True, description='task2 test', date = timezone.now())

    def test_puppy_breed(self):
        task_1 = Tasks.objects.get(title='task1')
        task_2 = Tasks.objects.get(title='task2')
        self.assertEqual(
            task_1.get_done(), False)
        self.assertEqual(
            task_2.get_done(), True)

