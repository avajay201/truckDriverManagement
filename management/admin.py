from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Count, Sum
from django.utils import timezone
from unfold.admin import ModelAdmin, TabularInline
from .models import Vehicle, Driver, Client, Route, Schedule, Shipment, Maintenance, DriverSalary, DriverAdvance, RouteCompletion

class MaintenanceInline(TabularInline):
    model = Maintenance
    extra = 0
    fields = ('maintenance_id', 'maintenance_type', 'start_date', 'status', 'cost')
    readonly_fields = ('maintenance_id',)

class ShipmentInline(TabularInline):
    model = Shipment
    extra = 0
    fields = ('shipment_id', 'client', 'status', 'pickup_date', 'delivery_date', 'price')
    readonly_fields = ('shipment_id',)

@admin.register(Vehicle)
class VehicleAdmin(ModelAdmin):
    list_display = ('vehicle_id', 'type', 'make', 'model', 'license_plate', 'status', 'current_mileage', 'display_image')
    list_filter = ('type', 'status', 'make', 'year', 'fuel_type')
    search_fields = ('vehicle_id', 'license_plate', 'vin', 'make', 'model')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Vehicle Information', {
            'fields': (('vehicle_id', 'status'), ('type', 'make', 'model', 'year'), 
                      ('license_plate', 'vin'), ('capacity', 'capacity_unit'))
        }),
        ('Financial Information', {
            'fields': (('purchase_date', 'purchase_price'),)
        }),
        ('Technical Information', {
            'fields': (('current_mileage', 'fuel_type', 'fuel_efficiency'),)
        }),
        ('Documentation', {
            'fields': (('insurance_expiry', 'registration_expiry'),)
        }),
        ('Additional Information', {
            'fields': ('notes', 'image', ('created_at', 'updated_at'))
        }),
    )
    inlines = [MaintenanceInline]
    
    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="auto" />', obj.image.url)
        return "No Image"
    display_image.short_description = 'Image'
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ('vehicle_id',)
        return self.readonly_fields

@admin.register(Driver)
class DriverAdmin(ModelAdmin):
    list_display = ('driver_id', 'full_name', 'license_type', 'license_expiry', 'status', 'display_photo')
    list_filter = ('status', 'license_type')
    search_fields = ('driver_id', 'first_name', 'last_name', 'license_number', 'phone_number', 'email')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Driver Information', {
            'fields': (('driver_id', 'status'), ('first_name', 'last_name'), 
                      ('date_of_birth', 'date_hired'), ('phone_number', 'email'))
        }),
        ('License Information', {
            'fields': (('license_number', 'license_type', 'license_expiry'),)
        }),
        ('Address & Emergency Contact', {
            'fields': ('address', ('emergency_contact_name', 'emergency_contact_phone'))
        }),
        ('Additional Information', {
            'fields': ('notes', 'photo', ('created_at', 'updated_at'))
        }),
        ('User Account', {
            'fields': ('user',),
            'classes': ('collapse',)
        }),
    )
    
    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = 'Name'
    
    def display_photo(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="50" height="auto" />', obj.photo.url)
        return "No Photo"
    display_photo.short_description = 'Photo'
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ('driver_id',)
        return self.readonly_fields

@admin.register(Client)
class ClientAdmin(ModelAdmin):
    list_display = ('client_id', 'name', 'contact_person', 'phone_number', 'email', 'is_active', 'shipment_count')
    list_filter = ('is_active', 'city', 'state', 'country')
    search_fields = ('client_id', 'name', 'contact_person', 'phone_number', 'email', 'address')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Client Information', {
            'fields': (('client_id', 'is_active'), ('name', 'contact_person'), 
                      ('phone_number', 'email'))
        }),
        ('Address Information', {
            'fields': ('address', ('city', 'state', 'postal_code'), 'country')
        }),
        ('Additional Information', {
            'fields': ('tax_id', 'notes', ('created_at', 'updated_at'))
        }),
    )
    inlines = [ShipmentInline]
    
    def shipment_count(self, obj):
        return obj.shipments.count()
    shipment_count.short_description = 'Shipments'
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ('client_id',)
        return self.readonly_fields
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(shipment_count=Count('shipments'))
        return queryset

@admin.register(Route)
class RouteAdmin(ModelAdmin):
    list_display = ('route_id', 'name', 'start_location', 'end_location', 'distance', 'estimated_duration', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('route_id', 'name', 'start_location', 'end_location')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Route Information', {
            'fields': (('route_id', 'is_active'), 'name', ('start_location', 'end_location'), 
                      ('distance', 'estimated_duration'))
        }),
        ('Additional Information', {
            'fields': ('description', ('created_at', 'updated_at'))
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ('route_id',)
        return self.readonly_fields

@admin.register(Schedule)
class ScheduleAdmin(ModelAdmin):
    list_display = ('schedule_id', 'route_display', 'vehicle_display', 'driver_display', 
                   'departure_time', 'arrival_time', 'frequency', 'status')
    list_filter = ('status', 'frequency', 'start_date')
    search_fields = ('schedule_id', 'route__name', 'vehicle__vehicle_id', 'driver__first_name', 'driver__last_name')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Schedule Information', {
            'fields': (('schedule_id', 'status'), ('route', 'vehicle', 'driver'), 
                      ('start_date', 'end_date'), ('departure_time', 'arrival_time'))
        }),
        ('Recurrence', {
            'fields': (('frequency', 'days_of_week'),)
        }),
        ('Additional Information', {
            'fields': ('notes', ('created_at', 'updated_at'))
        }),
    )
    inlines = [ShipmentInline]
    
    def route_display(self, obj):
        return format_html('<a href="{}">{}</a>', 
                          reverse('admin:tms_route_change', args=[obj.route.id]), 
                          obj.route.name)
    route_display.short_description = 'Route'
    
    def vehicle_display(self, obj):
        return format_html('<a href="{}">{}</a>', 
                          reverse('admin:tms_vehicle_change', args=[obj.vehicle.id]), 
                          obj.vehicle.vehicle_id)
    vehicle_display.short_description = 'Vehicle'
    
    def driver_display(self, obj):
        return format_html('<a href="{}">{} {}</a>', 
                          reverse('admin:tms_driver_change', args=[obj.driver.id]), 
                          obj.driver.first_name, obj.driver.last_name)
    driver_display.short_description = 'Driver'
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ('schedule_id',)
        return self.readonly_fields

@admin.register(Shipment)
class ShipmentAdmin(ModelAdmin):
    list_display = ('shipment_id', 'client_display', 'schedule_display', 'status', 
                   'pickup_date', 'delivery_date', 'price', 'payment_status')
    list_filter = ('status', 'payment_status', 'is_hazardous', 'is_fragile', 'is_perishable', 'requires_refrigeration')
    search_fields = ('shipment_id', 'tracking_number', 'client__name', 'pickup_location', 'delivery_location')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Shipment Information', {
            'fields': (('shipment_id', 'status'), ('client', 'schedule'), 
                      'description', ('weight', 'volume'))
        }),
        ('Pickup & Delivery', {
            'fields': (('pickup_location', 'delivery_location'), 
                      ('pickup_date', 'pickup_time'), 
                      ('delivery_date', 'delivery_time'))
        }),
        ('Tracking & Special Handling', {
            'fields': ('tracking_number', 'special_instructions', 
                      ('is_hazardous', 'is_fragile', 'is_perishable', 'requires_refrigeration'))
        }),
        ('Financial Information', {
            'fields': (('price', 'payment_status'),)
        }),
        ('Additional Information', {
            'fields': (('created_at', 'updated_at'),)
        }),
    )
    
    def client_display(self, obj):
        return format_html('<a href="{}">{}</a>', 
                          reverse('admin:tms_client_change', args=[obj.client.id]), 
                          obj.client.name)
    client_display.short_description = 'Client'
    
    def schedule_display(self, obj):
        return format_html('<a href="{}">{}</a>', 
                          reverse('admin:tms_schedule_change', args=[obj.schedule.id]), 
                          obj.schedule.schedule_id)
    schedule_display.short_description = 'Schedule'
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ('shipment_id',)
        return self.readonly_fields

@admin.register(Maintenance)
class MaintenanceAdmin(ModelAdmin):
    list_display = ('maintenance_id', 'vehicle_display', 'maintenance_type', 
                   'start_date', 'end_date', 'status', 'cost')
    list_filter = ('status', 'maintenance_type', 'start_date')
    search_fields = ('maintenance_id', 'vehicle__vehicle_id', 'description', 'service_provider')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Maintenance Information', {
            'fields': (('maintenance_id', 'status'), 'vehicle', 
                      'maintenance_type', 'description')
        }),
        ('Service Details', {
            'fields': (('start_date', 'end_date'), 
                      'mileage_at_service', 'service_provider', 'cost')
        }),
        ('Parts & Notes', {
            'fields': ('parts_replaced', 'notes')
        }),
        ('Additional Information', {
            'fields': (('created_at', 'updated_at'),)
        }),
    )
    
    def vehicle_display(self, obj):
        return format_html('<a href="{}">{}</a>', 
                          reverse('admin:tms_vehicle_change', args=[obj.vehicle.id]), 
                          obj.vehicle.vehicle_id)
    vehicle_display.short_description = 'Vehicle'
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ('maintenance_id',)
        return self.readonly_fields


class DriverSalaryInline(TabularInline):
    model = DriverSalary
    extra = 0
    fields = ('period_start', 'period_end', 'base_salary', 'bonus', 'deductions', 'total_amount', 'payment_status')
    readonly_fields = ('total_amount',)

class DriverAdvanceInline(TabularInline):
    model = DriverAdvance
    extra = 0
    fields = ('date_given', 'amount', 'purpose', 'amount_settled', 'status')
    readonly_fields = ('status',)

class RouteCompletionInline(TabularInline):
    model = RouteCompletion
    extra = 0
    fields = ('completion_date', 'schedule', 'distance_covered', 'earnings')

# Update the DriverAdmin to include these inlines
class DriverAdmin(ModelAdmin):
    # Keep your existing configuration and add:
    inlines = [DriverSalaryInline, DriverAdvanceInline, RouteCompletionInline]
    
    # Add these methods to DriverAdmin
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            total_earnings=Sum('route_completions__earnings', default=0),
            routes_completed=Count('route_completions', distinct=True),
            pending_advances=Sum('advances__amount', filter=models.Q(advances__status='PENDING'), default=0) - 
                            Sum('advances__amount_settled', filter=models.Q(advances__status='PENDING'), default=0)
        )
        return queryset
    
    def total_earnings(self, obj):
        return f"${obj.total_earnings}" if hasattr(obj, 'total_earnings') else "$0.00"
    total_earnings.short_description = "Total Earnings"
    total_earnings.admin_order_field = 'total_earnings'
    
    def routes_completed(self, obj):
        return obj.routes_completed if hasattr(obj, 'routes_completed') else 0
    routes_completed.short_description = "Routes Completed"
    routes_completed.admin_order_field = 'routes_completed'
    
    def pending_advances(self, obj):
        return f"${obj.pending_advances}" if hasattr(obj, 'pending_advances') else "$0.00"
    pending_advances.short_description = "Pending Advances"
    pending_advances.admin_order_field = 'pending_advances'
    
    # Update list_display to include these fields
    list_display = ('driver_id', 'full_name', 'license_type', 'status', 'routes_completed', 
                   'total_earnings', 'pending_advances', 'display_photo')

# Register the new models
@admin.register(DriverSalary)
class DriverSalaryAdmin(ModelAdmin):
    list_display = ('driver_display', 'period_type', 'period_start', 'period_end', 
                   'base_salary', 'bonus', 'deductions', 'total_amount', 'payment_status')
    list_filter = ('payment_status', 'period_type', 'period_start')
    search_fields = ('driver__first_name', 'driver__last_name', 'driver__driver_id')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Salary Information', {
            'fields': ('driver', ('period_type', 'period_start', 'period_end'))
        }),
        ('Payment Details', {
            'fields': (('base_salary', 'bonus', 'deductions'), 'total_amount', 
                      ('payment_date', 'payment_status'))
        }),
        ('Additional Information', {
            'fields': ('notes', ('created_at', 'updated_at'))
        }),
    )
    
    def driver_display(self, obj):
        return format_html('<a href="{}">{} {}</a>', 
                          reverse('admin:tms_driver_change', args=[obj.driver.id]), 
                          obj.driver.first_name, obj.driver.last_name)
    driver_display.short_description = 'Driver'
    driver_display.admin_order_field = 'driver__first_name'

@admin.register(DriverAdvance)
class DriverAdvanceAdmin(ModelAdmin):
    list_display = ('driver_display', 'amount', 'date_given', 'purpose', 
                   'amount_settled', 'pending_amount_display', 'status')
    list_filter = ('status', 'date_given')
    search_fields = ('driver__first_name', 'driver__last_name', 'driver__driver_id', 'purpose')
    readonly_fields = ('pending_amount_display', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Advance Information', {
            'fields': ('driver', ('amount', 'date_given'), 'purpose')
        }),
        ('Settlement Details', {
            'fields': (('amount_settled', 'pending_amount_display'), 
                      ('settlement_date', 'status'))
        }),
        ('Additional Information', {
            'fields': ('notes', ('created_at', 'updated_at'))
        }),
    )
    
    def driver_display(self, obj):
        return format_html('<a href="{}">{} {}</a>', 
                          reverse('admin:tms_driver_change', args=[obj.driver.id]), 
                          obj.driver.first_name, obj.driver.last_name)
    driver_display.short_description = 'Driver'
    driver_display.admin_order_field = 'driver__first_name'
    
    def pending_amount_display(self, obj):
        return obj.pending_amount
    pending_amount_display.short_description = 'Pending Amount'

@admin.register(RouteCompletion)
class RouteCompletionAdmin(ModelAdmin):
    list_display = ('driver_display', 'route_display', 'completion_date', 
                   'distance_covered', 'duration_display', 'earnings', 'is_completed')
    list_filter = ('is_completed', 'completion_date')
    search_fields = ('driver__first_name', 'driver__last_name', 'schedule__route__name')
    readonly_fields = ('duration_display', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Completion Information', {
            'fields': (('driver', 'schedule'), ('completion_date', 'is_completed'))
        }),
        ('Trip Details', {
            'fields': (('start_time', 'end_time', 'duration_display'), 
                      ('distance_covered', 'fuel_consumed'))
        }),
        ('Financial Details', {
            'fields': ('earnings',)
        }),
        ('Additional Information', {
            'fields': ('notes', ('created_at', 'updated_at'))
        }),
    )
    
    def driver_display(self, obj):
        return format_html('<a href="{}">{} {}</a>', 
                          reverse('admin:tms_driver_change', args=[obj.driver.id]), 
                          obj.driver.first_name, obj.driver.last_name)
    driver_display.short_description = 'Driver'
    driver_display.admin_order_field = 'driver__first_name'
    
    def route_display(self, obj):
        return format_html('<a href="{}">{}</a>', 
                          reverse('admin:tms_route_change', args=[obj.schedule.route.id]), 
                          obj.schedule.route.name)
    route_display.short_description = 'Route'
    route_display.admin_order_field = 'schedule__route__name'
    
    def duration_display(self, obj):
        return f"{obj.duration:.2f} hours"
    duration_display.short_description = 'Duration'