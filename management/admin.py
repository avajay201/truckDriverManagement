from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from .models import Dispatch, TruckDetail, HighwayUsage, Driver, VehicleMaintenance, Payment, CompanyInvoice, OffenceTicket, Record
from django.contrib.auth.models import User, Group


class TruckInline(TabularInline):
    model = TruckDetail
    extra = 1

class HighwayInline(TabularInline):
    model = HighwayUsage
    extra = 1

class DispatchAdmin(ModelAdmin):
    inlines = [TruckInline, HighwayInline]

class TruckDetailAdmin(ModelAdmin):
    pass

class HighwayUsageAdmin(ModelAdmin):
    pass

class DriverAdmin(ModelAdmin):
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
admin.site.register(TruckDetail, TruckDetailAdmin)
admin.site.register(HighwayUsage, HighwayUsageAdmin)
admin.site.register(Driver, DriverAdmin)
admin.site.register(VehicleMaintenance, VehicleMaintenanceAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(CompanyInvoice, CompanyInvoiceAdmin)
admin.site.register(OffenceTicket, OffenceTicketAdmin)
admin.site.register(Record, RecordAdmin)


admin.site.unregister(User)
admin.site.unregister(Group)

class UserAdmin(ModelAdmin):
    pass

class GroupAdmin(ModelAdmin):
    pass

admin.site.register(User, UserAdmin)
admin.site.register(Group, GroupAdmin)
