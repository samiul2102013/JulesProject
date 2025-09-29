from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, LessonViewSet, DeviceViewSet, TelemetryDataViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'lessons', LessonViewSet, basename='lesson')
router.register(r'devices', DeviceViewSet, basename='device')
router.register(r'telemetry', TelemetryDataViewSet, basename='telemetry')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
