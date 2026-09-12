from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from main.models import House, Availability


class HouseAccessTests(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create_user(username='user', password='secret123')
        self.admin = self.User.objects.create_user(username='admin', password='secret123', is_staff=True, is_superuser=True)
        self.availability = Availability.objects.create(assistance=False)
        self.house = House.objects.create(
            city='City',
            street='Street',
            number='1',
            floors=5,
            latitude=55.0,
            longitude=82.0,
            user=self.user,
            availability=self.availability,
        )

    def test_map_page_is_public(self):
        response = self.client.get(reverse('map'))
        self.assertEqual(response.status_code, 200)

    def test_create_house_requires_login(self):
        response = self.client.post(reverse('map'), {
            'city': 'Town',
            'street': 'Main',
            'number': '42',
            'floors': 4,
            'latitude': 55.1,
            'longitude': 82.1,
            'availability': self.availability.id,
        })

        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_non_admin_cannot_edit_existing_house(self):
        self.client.login(username='user', password='secret123')
        response = self.client.post(reverse('map'), {
            'house_id': self.house.id,
            'city': 'Changed',
            'street': 'Street',
            'number': '1',
            'floors': 6,
            'latitude': 55.0,
            'longitude': 82.0,
            'availability': self.availability.id,
        })

        self.assertEqual(response.status_code, 403)

    def test_admin_can_edit_existing_house(self):
        self.client.login(username='admin', password='secret123')
        response = self.client.post(reverse('map'), {
            'house_id': self.house.id,
            'city': 'Changed',
            'street': 'Street',
            'number': '1',
            'floors': 6,
            'latitude': 55.0,
            'longitude': 82.0,
            'availability': self.availability.id,
        })

        self.assertEqual(response.status_code, 302)
        self.house.refresh_from_db()
        self.assertEqual(self.house.city, 'Changed')
