from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Driver, Bus
from .serializers import DriverSerializer, BusSerializer

class IsAdminOrSuperUser(permissions.BasePermission):
    """
    Custom permission to only allow admin or superuser to access the view.
    """
    def has_permission(self, request, view):
        return request.user and (request.user.is_staff or request.user.is_superuser)

class DriverViewSet(viewsets.ModelViewSet):
    """
    API endpoint for CRUD operations on Driver model.
    Only accessible by admin or superuser.
    """
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    permission_classes = [IsAdminOrSuperUser]

class BusViewSet(viewsets.ModelViewSet):
    """
    API endpoint for CRUD operations on Bus model.
    Only accessible by admin or superuser.
    """
    queryset = Bus.objects.select_related('assigned_driver').all()
    serializer_class = BusSerializer
    permission_classes = [IsAdminOrSuperUser]

    def create(self, request, *args, **kwargs):
        """
        Create a new Bus instance. Handles assignment of driver by ID.
        """
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        Update an existing Bus instance. Handles assignment of driver by ID.
        """
        return super().update(request, *args, **kwargs)