from django.db import models


class Dispatch(models.Model):
    date = models.DateField()
    company_or_team = models.CharField(max_length=100)
    work_type = models.CharField(max_length=100)

    pickup_location = models.CharField(max_length=255)
    material_type = models.CharField(max_length=100)
    material_count = models.PositiveIntegerField()

    todays_bill = models.DecimalField(max_digits=10, decimal_places=2)
    previous_pending = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    amount_paid = models.BooleanField(default=False)
    paid_to = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.date} - {self.company_or_team}"

class TruckDetail(models.Model):
    dispatch = models.ForeignKey(Dispatch, on_delete=models.CASCADE, related_name='trucks')
    unit_number = models.CharField(max_length=100)
    license_plate = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    driver_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.unit_number} - {self.driver_name}"

class HighwayUsage(models.Model):
    dispatch = models.ForeignKey(Dispatch, on_delete=models.CASCADE, related_name='highway_trips')
    entry_location = models.CharField(max_length=100)
    exit_location = models.CharField(max_length=100)
    entry_time = models.TimeField()
    exit_time = models.TimeField()

    def __str__(self):
        return f"{self.entry_location} to {self.exit_location}"

class Driver(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    license_number = models.CharField(max_length=100)
    join_date = models.DateField()

    def __str__(self):
        return self.name

class VehicleMaintenance(models.Model):
    unit_number = models.CharField(max_length=100)
    license_plate = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    maintenance_date = models.DateField()
    issue_reported = models.TextField()
    maintenance_done = models.TextField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.unit_number} - {self.maintenance_date}"

class Payment(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField()
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.date} - {self.amount}"

class CompanyInvoice(models.Model):
    company_name = models.CharField(max_length=100)
    invoice_date = models.DateField()
    service_description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.company_name} - {self.invoice_date}"

class OffenceTicket(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True)
    vehicle_unit_number = models.CharField(max_length=100)
    offence_date = models.DateField()
    offence_type = models.CharField(max_length=100)
    fine_amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.driver} - {self.offence_type}"

class Record(models.Model):
    date = models.DateField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    document = models.FileField(upload_to='documents/', blank=True, null=True)

    def __str__(self):
        return self.title
