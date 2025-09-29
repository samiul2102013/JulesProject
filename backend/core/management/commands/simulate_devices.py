import random
import time
import sys
from django.core.management.base import BaseCommand
from core.models import Device, TelemetryData
from django.utils import timezone

class Command(BaseCommand):
    help = 'Simulates IoT devices sending telemetry data in a continuous loop.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting device simulation...'))

        # Create devices if they don't exist
        devices = self.get_or_create_devices()

        self.stdout.write(self.style.SUCCESS('Running continuous simulation. Press Ctrl+C to stop.'))

        try:
            while True:
                for device in devices:
                    self.create_telemetry_data(device)
                self.stdout.write(self.style.SUCCESS(f'Successfully sent new telemetry data for {len(devices)} devices.'))
                time.sleep(5)  # Wait for 5 seconds before the next iteration
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING('\nSimulation stopped by user.'))
            sys.exit(0)

        self.stdout.write(self.style.SUCCESS('Device simulation finished.'))

    def get_or_create_devices(self):
        """
        Retrieves or creates a predefined list of devices.
        """
        device_configs = [
            {'name': 'Conveyor-Belt-A1', 'device_type': 'Conveyor Belt'},
            {'name': 'Temperature-Sensor-Z3', 'device_type': 'Temperature Sensor'},
            {'name': 'Robotic-Arm-7', 'device_type': 'Robotic Arm'},
        ]

        devices = []
        for config in device_configs:
            device, created = Device.objects.get_or_create(
                name=config['name'],
                defaults={'device_type': config['device_type'], 'status': 'online'}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created device: {device.name}'))
            else:
                # Ensure device is marked as online for the simulation
                if device.status != 'online':
                    device.status = 'online'
                    device.save()
            devices.append(device)
        return devices

    def create_telemetry_data(self, device):
        """
        Creates a single telemetry data point for a given device.
        """
        if device.device_type == 'Temperature Sensor':
            data = {
                'temperature': round(random.uniform(20.0, 30.0), 2),
                'humidity': round(random.uniform(40.0, 60.0), 2),
            }
        elif device.device_type == 'Conveyor Belt':
            data = {
                'speed': round(random.uniform(0.5, 2.0), 2),
                'vibration': round(random.uniform(0.1, 0.5), 4),
            }
        else: # Robotic Arm
            data = {
                'position_x': random.randint(100, 500),
                'position_y': random.randint(100, 500),
                'load_kg': round(random.uniform(5.0, 15.0), 2),
            }

        TelemetryData.objects.create(device=device, data=data)