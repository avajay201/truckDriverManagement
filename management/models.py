from django.db import models

class Driver(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    license_number = models.CharField(max_length=50, unique=True)
    address = models.TextField()
    date_of_birth = models.DateField()
    experience_years = models.PositiveIntegerField()
    monthly_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
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
    base_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    estimated_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

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
    advance_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    fuel_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    toll_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    misc_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.driver.name} - {self.truck.registration_number} on {self.route}"

class DriverPayment(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.driver.name} - {self.amount} on {self.date}"
