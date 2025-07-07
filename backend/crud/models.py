from django.db import models


class Driver(models.Model):
    """
    Model representing a driver.
    Fields:
        driver_id: Auto-incremented primary key for the driver.
        name: Name of the driver.
        phone_number: Contact number of the driver.
    """
    driver_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)

    class Meta:
        verbose_name = "Driver"
        verbose_name_plural = "Drivers"
        ordering = ["name"]

    def __str__(self):
        return self.name



class Bus(models.Model):
    """
    Model representing a bus.
    Fields:
        bus_name: Name of the bus.
        route: Route of the bus.
        assigned_driver: ForeignKey to Driver, can be null if not assigned.
    """
    bus_name = models.CharField(max_length=100)
    route = models.CharField(max_length=200)
    assigned_driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True, related_name='buses')

    class Meta:
        verbose_name = "Bus"
        verbose_name_plural = "Buses"
        ordering = ["bus_name"]

    def __str__(self):
        return self.bus_name
