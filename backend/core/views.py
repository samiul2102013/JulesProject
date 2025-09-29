from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Course, Lesson, Device, TelemetryData
from .serializers import CourseSerializer, LessonSerializer, DeviceSerializer, TelemetryDataSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows courses to be viewed or edited.
    """
    queryset = Course.objects.all().order_by('-created_at')
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class LessonViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows lessons to be viewed or edited.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class DeviceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows devices to be viewed or edited.
    """
    queryset = Device.objects.all().order_by('created_at')
    serializer_class = DeviceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class TelemetryDataViewSet(viewsets.ModelViewSet):
    """
    API endpoint for viewing and creating telemetry data.
    """
    queryset = TelemetryData.objects.all().order_by('-timestamp')
    serializer_class = TelemetryDataSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """
        Optionally restricts the returned telemetry data to a given device,
        by filtering against a `device` query parameter in the URL.
        """
        queryset = super().get_queryset()
        device_id = self.request.query_params.get('device_id')
        if device_id:
            queryset = queryset.filter(device_id=device_id)
        return queryset
