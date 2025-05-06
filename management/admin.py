from django.contrib import admin
from .models import Driver, Truck, Route, Assignment

@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone_number', 'license_number', 'experience_years', 'is_active']
    search_fields = ['name', 'license_number']


@admin.register(Truck)
class TruckAdmin(admin.ModelAdmin):
    list_display = ['registration_number', 'model', 'capacity_in_tons', 'is_available']
    search_fields = ['registration_number']


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ['source', 'destination', 'distance_km']
    search_fields = ['source', 'destination']


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['driver', 'truck', 'route', 'start_date', 'end_date', 'status']
    list_filter = ['status', 'start_date']
