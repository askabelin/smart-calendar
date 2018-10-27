from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter(trailing_slash=False)
router.register(r'available-slots', views.AvailableSlotsViewSet, basename='available')
router.register(r'interview-slots', views.InterviewSlotsViewSet, basename='interview')

urlpatterns = [
    path('', include(router.urls)),
]
