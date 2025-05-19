from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from .models import Dispatch, TruckDetail, HighwayUsage, Employee, VehicleMaintenance, Payment, CompanyInvoice, OffenceTicket, Record


class TruckInline(TabularInline):
    model = TruckDetail
    extra = 1

class HighwayInline(TabularInline):
    model = HighwayUsage
    extra = 1

class DispatchAdmin(ModelAdmin):
    inlines = [TruckInline, HighwayInline]

class EmployeeAdmin(ModelAdmin):
    pass

class VehicleMaintenanceAdmin(ModelAdmin):
    pass

class PaymentAdmin(ModelAdmin):
    pass

class CompanyInvoiceAdmin(ModelAdmin):
    pass

class OffenceTicketAdmin(ModelAdmin):
    pass

class RecordAdmin(ModelAdmin):
    pass


admin.site.register(Dispatch, DispatchAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(VehicleMaintenance, VehicleMaintenanceAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(CompanyInvoice, CompanyInvoiceAdmin)
admin.site.register(OffenceTicket, OffenceTicketAdmin)
admin.site.register(Record, RecordAdmin)
