from django.db import models

class Driver(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    license_number = models.CharField(max_length=50, unique=True)
    address = models.TextField()
    date_of_birth = models.DateField()
    experience_years = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Truck(models.Model):
    registration_number = models.CharField(max_length=20, unique=True)
    model = models.CharField(max_length=100)
    capacity_in_tons = models.FloatField()
    manufacturer = models.CharField(max_length=100)
    year_of_manufacture = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.registration_number


class Route(models.Model):
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    distance_km = models.FloatField()
    expected_travel_time_hrs = models.FloatField()
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.source} to {self.destination}"


class Assignment(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=[
        ("Scheduled", "Scheduled"),
        ("In Transit", "In Transit"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    ])

    def __str__(self):
        return f"{self.driver.name} - {self.truck.registration_number} on {self.route}"
