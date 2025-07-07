
from rest_framework import serializers
from .models import Driver, Bus


class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ['driver_id', 'name', 'phone_number']
        read_only_fields = ['driver_id']
        extra_kwargs = {
            'name': {'required': True},
            'phone_number': {'required': True}
        }

    def validate_phone_number(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Phone number must contain only digits.")
        if len(value) < 7 or len(value) > 15:
            raise serializers.ValidationError("Phone number must be between 7 and 15 digits.")
        return value



class BusSerializer(serializers.ModelSerializer):
    assigned_driver = DriverSerializer(read_only=True)
    assigned_driver_id = serializers.PrimaryKeyRelatedField(
        queryset=Driver.objects.all(), source='assigned_driver', write_only=True, required=False, allow_null=True
    )

    class Meta:
        model = Bus
        fields = ['id', 'bus_name', 'route', 'assigned_driver', 'assigned_driver_id']
        read_only_fields = ['id', 'assigned_driver']
        extra_kwargs = {
            'bus_name': {'required': True},
            'route': {'required': True}
        }

    def validate(self, data):
        bus_name = data.get('bus_name')
        route = data.get('route')
        assigned_driver = data.get('assigned_driver')
        if bus_name and len(bus_name.strip()) == 0:
            raise serializers.ValidationError({"bus_name": "Bus name cannot be empty."})
        if route and len(route.strip()) == 0:
            raise serializers.ValidationError({"route": "Route cannot be empty."})
        # Validate assigned_driver exists if provided
        if assigned_driver is not None:
            from .models import Driver
            if not Driver.objects.filter(pk=assigned_driver.pk).exists():
                raise serializers.ValidationError({"assigned_driver_id": "Assigned driver does not exist."})
        return data
