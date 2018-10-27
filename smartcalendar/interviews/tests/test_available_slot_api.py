from datetime import datetime, timedelta

from django.contrib.auth.models import User
from rest_framework.test import APITestCase


class AvailableSlotsAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username='user')
        self.client.force_login(self.user)

    def test_create(self):
        start = datetime.now().replace(minute=0) + timedelta(days=1)
        end = start + timedelta(hours=3)
        request_data = {
            'start': start.isoformat(),
            'end': end.isoformat()
        }
        response = self.client.post('/available-slots', request_data)
        self.assertEqual(response.status_code, 201)
        created_slots = self.user.slots.all()
        self.assertEqual(created_slots.count(), 3)
        self.assertEqual(created_slots[0].start, start)
        self.assertEqual(created_slots[1].start, start + timedelta(hours=1))
        self.assertEqual(created_slots[2].start, start + timedelta(hours=2))

    def test_create_partial(self):
        start = datetime.now().replace(minute=20) + timedelta(days=1)
        end = start + timedelta(hours=3)
        request_data = {
            'start': start.isoformat(),
            'end': end.isoformat()
        }
        response = self.client.post('/available-slots', request_data)
        self.assertEqual(response.status_code, 201)
        sharp_start = start.replace(minute=0) + timedelta(hours=1)
        created_slots = self.user.slots.all()
        self.assertEqual(created_slots.count(), 2)
        self.assertEqual(created_slots[0].start, sharp_start)
        self.assertEqual(created_slots[1].start, sharp_start + timedelta(hours=1))

    def test_create_in_past(self):
        request_data = {
            'start': datetime(2018, 1, 1).isoformat(),
            'end': datetime(2018, 1, 1, 1).isoformat()
        }
        response = self.client.post('/available-slots', request_data)
        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        self.assertIn('should be in future', response_data['start'][0])
        self.assertIn('should be in future', response_data['end'][0])

    def test_end_before_start(self):
        start = datetime.now() + timedelta(days=1)
        end = start - timedelta(hours=1)
        request_data = {
            'start': start.isoformat(),
            'end': end.isoformat()
        }
        response = self.client.post('/available-slots', request_data)
        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        self.assertIn('end should be later than start', response_data['non_field_errors'][0])

    def test_create_too_short_slot(self):
        start = datetime.now() + timedelta(days=1)
        end = start + timedelta(minutes=50)
        request_data = {
            'start': start.isoformat(),
            'end': end.isoformat()
        }
        response = self.client.post('/available-slots', request_data)
        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        self.assertIn('slot is too short', response_data['non_field_errors'][0])
