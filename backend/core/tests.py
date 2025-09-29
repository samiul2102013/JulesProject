from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Device, TelemetryData
import json

class DeviceModelTest(TestCase):
    def test_device_creation(self):
        device = Device.objects.create(name="Test Device", device_type="sensor")
        self.assertEqual(device.name, "Test Device")
        self.assertEqual(device.status, 'offline')

class TelemetryDataModelTest(TestCase):
    def setUp(self):
        self.device = Device.objects.create(name="Test Device", device_type="sensor")

    def test_telemetry_data_creation(self):
        telemetry_data = {"temperature": 25.5, "humidity": 60.2}
        telemetry = TelemetryData.objects.create(
            device=self.device,
            data=telemetry_data
        )
        self.assertEqual(telemetry.device.name, "Test Device")
        self.assertEqual(telemetry.data['temperature'], 25.5)

class DeviceAPITest(APITestCase):
    def setUp(self):
        self.device1 = Device.objects.create(name="Device 1", device_type="actuator")
        self.device2 = Device.objects.create(name="Device 2", device_type="sensor")

    def test_get_device_list(self):
        url = reverse('device-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['name'], 'Device 1')

class TelemetryAPITest(APITestCase):
    def setUp(self):
        self.device = Device.objects.create(name="Test Device", device_type="sensor")
        TelemetryData.objects.create(
            device=self.device,
            data={"temperature": 25.5, "humidity": 60.2}
        )
        TelemetryData.objects.create(
            device=self.device,
            data={"temperature": 25.6, "humidity": 60.3}
        )

    def test_get_telemetry_for_device(self):
        url = reverse('telemetry-list')
        response = self.client.get(url, {'device_id': self.device.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        # The data from the API will be a string, so we parse it
        self.assertEqual(response.data[0]['data']['temperature'], 25.6) # ordered by -timestamp
        self.assertEqual(response.data[1]['data']['temperature'], 25.5)