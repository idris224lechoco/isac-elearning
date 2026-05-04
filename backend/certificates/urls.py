from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CertificateViewSet, CertificateVerificationView

router = DefaultRouter()
router.register(r'certificates', CertificateViewSet, basename='certificate')
router.register(r'certificates/verify', CertificateVerificationView, basename='verify')

urlpatterns = [
    path('', include(router.urls)),
]
