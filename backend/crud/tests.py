
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from .models import Driver, Bus

class DriverBusAPITestCase(APITestCase):
    """
    Test suite for Driver and Bus API endpoints with admin authentication.
    """
    def setUp(self):
        self.admin_user = User.objects.create_superuser(username='admin', password='adminpass', email='admin@example.com')
        self.token, _ = Token.objects.get_or_create(user=self.admin_user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        # Create a driver
        self.driver = Driver.objects.create(name='John Doe', phone_number='1234567890')
        # Create a bus
        self.bus = Bus.objects.create(bus_name='Bus 1', route='Route 1', assigned_driver=self.driver)

    def test_get_all_drivers(self):
        response = self.client.get('/api/drivers/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # DRF DefaultRouter returns a list, but if pagination is enabled, it's a dict with 'results'
        if isinstance(response.data, dict) and 'results' in response.data:
            self.assertIsInstance(response.data['results'], list)
        else:
            self.assertIsInstance(response.data, list)

    def test_get_one_driver(self):
        response = self.client.get(f'/api/drivers/{self.driver.driver_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.driver.name)

    def test_create_driver(self):
        data = {
            'name': 'Jane Smith',
            'phone_number': '9876543210'
        }
        response = self.client.post('/api/drivers/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Jane Smith')

    def test_update_driver(self):
        data = {
            'name': 'John Updated',
            'phone_number': '1234567890'
        }
        response = self.client.put(f'/api/drivers/{self.driver.driver_id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'John Updated')

    def test_delete_driver(self):
        response = self.client.delete(f'/api/drivers/{self.driver.driver_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_driver_invalid_phone(self):
        data = {
            'name': 'Invalid Phone',
            'phone_number': 'abc123'
        }
        response = self.client.post('/api/drivers/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('phone_number', response.data)

    def test_get_all_buses(self):
        response = self.client.get('/api/buses/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if isinstance(response.data, dict) and 'results' in response.data:
            self.assertIsInstance(response.data['results'], list)
        else:
            self.assertIsInstance(response.data, list)

    def test_get_one_bus(self):
        response = self.client.get(f'/api/buses/{self.bus.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['bus_name'], self.bus.bus_name)

    def test_create_bus(self):
        data = {
            'bus_name': 'Bus 2',
            'route': 'Route 2',
            'assigned_driver_id': self.driver.driver_id
        }
        response = self.client.post('/api/buses/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['bus_name'], 'Bus 2')

    def test_update_bus(self):
        data = {
            'bus_name': 'Bus Updated',
            'route': 'Route Updated',
            'assigned_driver_id': self.driver.driver_id
        }
        response = self.client.put(f'/api/buses/{self.bus.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['bus_name'], 'Bus Updated')

    def test_delete_bus(self):
        response = self.client.delete(f'/api/buses/{self.bus.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_bus_with_invalid_driver(self):
        data = {
            'bus_name': 'Bus 3',
            'route': 'Route 3',
            'assigned_driver_id': 9999  # Non-existent driver
        }
        response = self.client.post('/api/buses/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('assigned_driver_id', response.data)
