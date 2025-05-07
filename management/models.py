from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone
import datetime
from django.contrib.auth.models import User

class Vehicle(models.Model):
    VEHICLE_TYPES = [
        ('TRUCK', 'Truck'),
        ('VAN', 'Van'),
        ('BUS', 'Bus'),
        ('CAR', 'Car'),
        ('MOTORCYCLE', 'Motorcycle'),
        ('OTHER', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('MAINTENANCE', 'Under Maintenance'),
        ('INACTIVE', 'Inactive'),
        ('RETIRED', 'Retired'),
    ]
    
    vehicle_id = models.CharField(max_length=20, unique=True, verbose_name="Vehicle ID")
    type = models.CharField(max_length=20, choices=VEHICLE_TYPES)
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.PositiveIntegerField()
    license_plate = models.CharField(max_length=20, unique=True)
    vin = models.CharField(max_length=17, unique=True, verbose_name="VIN")
    capacity = models.DecimalField(max_digits=10, decimal_places=2, help_text="Capacity in tons or passengers")
    capacity_unit = models.CharField(max_length=10, choices=[('TONS', 'Tons'), ('PASSENGERS', 'Passengers')], default='TONS')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    purchase_date = models.DateField()
    purchase_price = models.DecimalField(max_digits=12, decimal_places=2)
    current_mileage = models.PositiveIntegerField(help_text="Current mileage in kilometers")
    fuel_type = models.CharField(max_length=20, choices=[
        ('DIESEL', 'Diesel'),
        ('PETROL', 'Petrol/Gasoline'),
        ('ELECTRIC', 'Electric'),
        ('HYBRID', 'Hybrid'),
        ('CNG', 'CNG'),
        ('LPG', 'LPG'),
    ])
    fuel_efficiency = models.DecimalField(max_digits=5, decimal_places=2, help_text="Fuel efficiency in km/l or km/kWh")
    insurance_expiry = models.DateField()
    registration_expiry = models.DateField()
    notes = models.TextField(blank=True)
    image = models.ImageField(upload_to='vehicles/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.vehicle_id} - {self.make} {self.model} ({self.license_plate})"
    
    class Meta:
        verbose_name = "Vehicle"
        verbose_name_plural = "Vehicles"
        ordering = ['vehicle_id']


class Driver(models.Model):
    LICENSE_TYPES = [
        ('A', 'Class A - Heavy Vehicles'),
        ('B', 'Class B - Medium Vehicles'),
        ('C', 'Class C - Light Vehicles'),
        ('D', 'Class D - Passenger Vehicles'),
        ('E', 'Class E - Special Vehicles'),
    ]
    
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('ON_LEAVE', 'On Leave'),
        ('INACTIVE', 'Inactive'),
        ('TERMINATED', 'Terminated'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    driver_id = models.CharField(max_length=20, unique=True, verbose_name="Driver ID")
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17)
    email = models.EmailField()
    address = models.TextField()
    date_of_birth = models.DateField()
    license_number = models.CharField(max_length=50, unique=True)
    license_type = models.CharField(max_length=1, choices=LICENSE_TYPES)
    license_expiry = models.DateField()
    date_hired = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    emergency_contact_name = models.CharField(max_length=100)
    emergency_contact_phone = models.CharField(validators=[phone_regex], max_length=17)
    notes = models.TextField(blank=True)
    photo = models.ImageField(upload_to='drivers/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.driver_id} - {self.first_name} {self.last_name}"
    
    class Meta:
        verbose_name = "Driver"
        verbose_name_plural = "Drivers"
        ordering = ['driver_id']


class Client(models.Model):
    client_id = models.CharField(max_length=20, unique=True, verbose_name="Client ID")
    name = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=100)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17)
    email = models.EmailField()
    address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=50)
    tax_id = models.CharField(max_length=50, blank=True)
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.client_id} - {self.name}"
    
    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"
        ordering = ['client_id']


class Route(models.Model):
    route_id = models.CharField(max_length=20, unique=True, verbose_name="Route ID")
    name = models.CharField(max_length=100)
    start_location = models.CharField(max_length=100)
    end_location = models.CharField(max_length=100)
    distance = models.DecimalField(max_digits=10, decimal_places=2, help_text="Distance in kilometers")
    estimated_duration = models.DurationField(help_text="Estimated duration in hours and minutes")
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.route_id} - {self.name} ({self.start_location} to {self.end_location})"
    
    class Meta:
        verbose_name = "Route"
        verbose_name_plural = "Routes"
        ordering = ['route_id']


class Schedule(models.Model):
    FREQUENCY_CHOICES = [
        ('DAILY', 'Daily'),
        ('WEEKLY', 'Weekly'),
        ('BIWEEKLY', 'Bi-weekly'),
        ('MONTHLY', 'Monthly'),
        ('CUSTOM', 'Custom'),
    ]
    
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
        ('COMPLETED', 'Completed'),
    ]
    
    schedule_id = models.CharField(max_length=20, unique=True, verbose_name="Schedule ID")
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='schedules')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='schedules')
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='schedules')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
    days_of_week = models.CharField(max_length=20, blank=True, help_text="For weekly schedules, comma-separated days (e.g., 'MON,WED,FRI')")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.schedule_id} - {self.route.name} ({self.departure_time})"
    
    class Meta:
        verbose_name = "Schedule"
        verbose_name_plural = "Schedules"
        ordering = ['schedule_id']


class Shipment(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_TRANSIT', 'In Transit'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
        ('DELAYED', 'Delayed'),
    ]
    
    shipment_id = models.CharField(max_length=20, unique=True, verbose_name="Shipment ID")
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='shipments')
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='shipments')
    description = models.TextField()
    weight = models.DecimalField(max_digits=10, decimal_places=2, help_text="Weight in kg")
    volume = models.DecimalField(max_digits=10, decimal_places=2, help_text="Volume in cubic meters", null=True, blank=True)
    pickup_location = models.CharField(max_length=200)
    delivery_location = models.CharField(max_length=200)
    pickup_date = models.DateField()
    pickup_time = models.TimeField()
    delivery_date = models.DateField()
    delivery_time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    tracking_number = models.CharField(max_length=50, unique=True)
    special_instructions = models.TextField(blank=True)
    is_hazardous = models.BooleanField(default=False)
    is_fragile = models.BooleanField(default=False)
    is_perishable = models.BooleanField(default=False)
    requires_refrigeration = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    payment_status = models.CharField(max_length=20, choices=[
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('PARTIAL', 'Partially Paid'),
        ('OVERDUE', 'Overdue'),
    ], default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.shipment_id} - {self.client.name} ({self.status})"
    
    class Meta:
        verbose_name = "Shipment"
        verbose_name_plural = "Shipments"
        ordering = ['shipment_id']


class Maintenance(models.Model):
    MAINTENANCE_TYPES = [
        ('ROUTINE', 'Routine Maintenance'),
        ('REPAIR', 'Repair'),
        ('INSPECTION', 'Inspection'),
        ('EMERGENCY', 'Emergency Repair'),
        ('OTHER', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('SCHEDULED', 'Scheduled'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    maintenance_id = models.CharField(max_length=20, unique=True, verbose_name="Maintenance ID")
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='maintenance_records')
    maintenance_type = models.CharField(max_length=20, choices=MAINTENANCE_TYPES)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    mileage_at_service = models.PositiveIntegerField()
    cost = models.DecimalField(max_digits=12, decimal_places=2)
    service_provider = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='SCHEDULED')
    parts_replaced = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.maintenance_id} - {self.vehicle.vehicle_id} ({self.maintenance_type})"
    
    class Meta:
        verbose_name = "Maintenance Record"
        verbose_name_plural = "Maintenance Records"
        ordering = ['maintenance_id']


class RouteCompletion(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='route_completions')
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='completions')
    completion_date = models.DateField()
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    distance_covered = models.DecimalField(max_digits=10, decimal_places=2, help_text="Distance in kilometers")
    fuel_consumed = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Fuel consumed in liters")
    earnings = models.DecimalField(max_digits=10, decimal_places=2, help_text="Driver's earnings for this route")
    is_completed = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def duration(self):
        """Calculate the duration of the route in hours."""
        if self.start_time is None or self.end_time is None:
            return 0  # Return 0 instead of None

        # Combine date and time to create datetime objects
        start_dt = datetime.datetime.combine(datetime.date.today(), self.start_time)
        end_dt = datetime.datetime.combine(datetime.date.today(), self.end_time)

        # If end time is earlier than start time, it means it's on the next day
        if end_dt < start_dt:  
            end_dt += datetime.timedelta(days=1)
        
        # Calculate and return duration in hours
        duration_hours = (end_dt - start_dt).total_seconds() / 3600  # Return hours
        return round(duration_hours, 2)  # Optional: rounding to 2 decimal places
    
    def __str__(self):
        return f"{self.driver.first_name} {self.driver.last_name} - {self.schedule.route.name} ({self.completion_date})"
    
    class Meta:
        verbose_name = "Route Completion"
        verbose_name_plural = "Route Completions"
        ordering = ['-completion_date']
class DriverSalary(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('PARTIAL', 'Partially Paid'),
    ]
    
    PERIOD_CHOICES = [
        ('WEEKLY', 'Weekly'),
        ('BIWEEKLY', 'Bi-weekly'),
        ('MONTHLY', 'Monthly'),
    ]
    
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='salaries')
    period_start = models.DateField()
    period_end = models.DateField()
    period_type = models.CharField(max_length=10, choices=PERIOD_CHOICES, default='MONTHLY')
    base_salary = models.DecimalField(max_digits=10, decimal_places=2)
    bonus = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(null=True, blank=True)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='PENDING')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.driver.first_name} {self.driver.last_name} - {self.period_start} to {self.period_end}"
    
    def save(self, *args, **kwargs):
        # Calculate total amount if not set
        if not self.total_amount:
            self.total_amount = self.base_salary + self.bonus - self.deductions
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Driver Salary"
        verbose_name_plural = "Driver Salaries"
        ordering = ['-period_end', 'driver']

class DriverAdvance(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SETTLED', 'Settled'),
        ('PARTIALLY_SETTLED', 'Partially Settled'),
    ]
    
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='advances')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_given = models.DateField()
    purpose = models.CharField(max_length=200)
    amount_settled = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    settlement_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def pending_amount(self):
        if self.amount is None or self.amount_settled is None:
            return 0
    
    def __str__(self):
        return f"{self.driver.first_name} {self.driver.last_name} - {self.amount} ({self.date_given})"
    
    def save(self, *args, **kwargs):
        # Update status based on settlement
        if self.amount_settled >= self.amount:
            self.status = 'SETTLED'
            if not self.settlement_date:
                self.settlement_date = timezone.now().date()
        elif self.amount_settled > 0:
            self.status = 'PARTIALLY_SETTLED'
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Driver Advance"
        verbose_name_plural = "Driver Advances"
        ordering = ['-date_given']