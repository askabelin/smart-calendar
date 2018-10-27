from datetime import datetime

from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from ..models import get_candidates_group, get_interviewers_group


class InterviewSlotsAPITestCase(APITestCase):

    def test_one_interviewer(self):
        candidate = User.objects.create(username='candidate')
        candidate.groups.add(get_candidates_group())
        candidate.slots.create(start=datetime(2018, 10, 26, 10))
        candidate.slots.create(start=datetime(2018, 10, 26, 11))
        candidate.slots.create(start=datetime(2018, 10, 26, 12))

        interviewer = User.objects.create(username='interviewer')
        interviewer.groups.add(get_interviewers_group())
        interviewer.slots.create(start=datetime(2018, 10, 26, 11))
        interviewer.slots.create(start=datetime(2018, 10, 26, 12))
        interviewer.slots.create(start=datetime(2018, 10, 26, 13))
        interviewer.slots.create(start=datetime(2018, 10, 26, 14))

        response = self.client.get(f'/interview-slots/{candidate.pk}', {'interviewers': [interviewer.pk]})
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data, [
            {'start': datetime(2018, 10, 26, 11).isoformat(), 'end': datetime(2018, 10, 26, 12).isoformat()},
            {'start': datetime(2018, 10, 26, 12).isoformat(), 'end': datetime(2018, 10, 26, 13).isoformat()},
        ])

    def test_two_interviewers(self):
        candidate = User.objects.create(username='candidate')
        candidate.groups.add(get_candidates_group())
        candidate.slots.create(start=datetime(2018, 10, 26, 11))
        candidate.slots.create(start=datetime(2018, 10, 26, 12))
        candidate.slots.create(start=datetime(2018, 10, 26, 13))
        candidate.slots.create(start=datetime(2018, 10, 26, 14))
        candidate.slots.create(start=datetime(2018, 10, 26, 15))
        candidate.slots.create(start=datetime(2018, 10, 26, 16))  # <- match

        interviewer1 = User.objects.create(username='interviewer1')
        interviewer1.groups.add(get_interviewers_group())
        interviewer1.slots.create(start=datetime(2018, 10, 26, 11))
        interviewer1.slots.create(start=datetime(2018, 10, 26, 12))
        interviewer1.slots.create(start=datetime(2018, 10, 26, 16))  # <- match
        interviewer1.slots.create(start=datetime(2018, 10, 26, 17))
        interviewer1.slots.create(start=datetime(2018, 10, 26, 18))

        interviewer2 = User.objects.create(username='interviewer2')
        interviewer2.groups.add(get_interviewers_group())
        interviewer2.slots.create(start=datetime(2018, 10, 26, 14))
        interviewer2.slots.create(start=datetime(2018, 10, 26, 15))
        interviewer2.slots.create(start=datetime(2018, 10, 26, 16))  # <- match

        response = self.client.get(f'/interview-slots/{candidate.pk}',
                                   {'interviewers': [interviewer1.pk, interviewer2.pk]})
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data, [
            {'start': datetime(2018, 10, 26, 16).isoformat(), 'end': datetime(2018, 10, 26, 17).isoformat()},
        ])

    def test_non_existing_candidate(self):
        response = self.client.get('/interview-slots/999')
        self.assertEqual(response.status_code, 404)
