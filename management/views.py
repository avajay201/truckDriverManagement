from django.shortcuts import render
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from .models import Driver, TruckDetail


def welcome(request):
    return render(request, 'welcome.html')

def generate_report(request):
    if request.method == "POST":
        selection = request.POST.get("report_type")
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{selection}_report.pdf"'

        p = canvas.Canvas(response)
        p.setFont("Helvetica", 14)
        p.drawString(100, 800, f"{selection.capitalize()} Report")

        y = 760

        if selection == "driver":
            drivers = Driver.objects.all()
            for driver in drivers:
                line = f"Name: {driver.name}, Position: {driver.position}, Phone: {driver.phone}"
                p.drawString(50, y, line)
                y -= 20

        elif selection == "truck":
            trucks = TruckDetail.objects.all()
            for truck in trucks:
                line = f"Unit: {truck.unit_number}, License: {truck.license_plate}, Driver: {truck.driver_name}"
                p.drawString(50, y, line)
                y -= 20

        p.showPage()
        p.save()
        return response

    return render(request, "custom_dashboard.html")
