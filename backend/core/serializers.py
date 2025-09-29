from rest_framework import serializers
from .models import Course, Lesson, CustomUser

class LessonSerializer(serializers.ModelSerializer):
    """
    Serializer for the Lesson model.
    """
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'content', 'order']

from .models import Device, TelemetryData


class CourseSerializer(serializers.ModelSerializer):
    """
    Serializer for the Course model. Includes nested lessons.
    """
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'created_at', 'updated_at', 'lessons']


class TelemetryDataSerializer(serializers.ModelSerializer):
    """
    Serializer for the TelemetryData model.
    """
    class Meta:
        model = TelemetryData
        fields = ['id', 'device', 'timestamp', 'data']


class DeviceSerializer(serializers.ModelSerializer):
    """
    Serializer for the Device model.
    Includes the latest 10 telemetry data points for a quick overview.
    """
    telemetry = TelemetryDataSerializer(many=True, read_only=True)

    class Meta:
        model = Device
        fields = ['id', 'name', 'device_type', 'status', 'created_at', 'updated_at', 'telemetry']

    def to_representation(self, instance):
        """
        Limit the nested telemetry data to the latest 10 records for efficiency.
        """
        representation = super().to_representation(instance)
        # Efficiently fetch the latest 10 records directly from the database
        latest_telemetry = instance.telemetry.order_by('-timestamp')[:10]
        representation['telemetry'] = TelemetryDataSerializer(latest_telemetry, many=True).data
        return representation
