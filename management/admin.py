from django.contrib import admin
from .models import Driver, Truck, Route, Assignment, DriverPayment

# ─────────────── DRIVER ───────────────
@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ("name", "phone_number", "license_number", "monthly_salary", "is_active")
    search_fields = ("name", "phone_number", "license_number", "email")
    list_filter = ("is_active", "experience_years")
    ordering = ("name",)


# ─────────────── TRUCK ───────────────
@admin.register(Truck)
class TruckAdmin(admin.ModelAdmin):
    list_display = ("registration_number", "model", "capacity_in_tons", "is_available")
    search_fields = ("registration_number", "model", "manufacturer")
    list_filter = ("is_available", "year_of_manufacture")


# ─────────────── ROUTE ───────────────
@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ("source", "destination", "distance_km", "base_price", "estimated_spent")
    search_fields = ("source", "destination")
    list_filter = ("source", "destination")


# ─────────────── INLINE PAYMENT ───────────────
class DriverPaymentInline(admin.TabularInline):
    model = DriverPayment
    extra = 1


# ─────────────── ASSIGNMENT ───────────────
@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = (
        "driver", "truck", "route", "start_date", "end_date", "status",
        "advance_paid", "fuel_spent", "toll_spent", "misc_spent",
        "total_spent_display", "remaining_salary_display"
    )
    list_filter = ("status", "start_date", "end_date", "driver__name")
    search_fields = ("driver__name", "truck__registration_number", "route__source", "route__destination")
    inlines = [DriverPaymentInline]

    @admin.display(description="Total Spent")
    def total_spent_display(self, obj):
        return obj.fuel_spent + obj.toll_spent + obj.misc_spent

    @admin.display(description="Remaining Salary")
    def remaining_salary_display(self, obj):
        return max(obj.driver.monthly_salary - obj.advance_paid, 0)


# ─────────────── DRIVER PAYMENT ───────────────
@admin.register(DriverPayment)
class DriverPaymentAdmin(admin.ModelAdmin):
    list_display = ("driver", "assignment", "amount", "date", "description")
    search_fields = ("driver__name", "assignment__driver__name")
    list_filter = ("date", "driver")
