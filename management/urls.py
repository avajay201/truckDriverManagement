from django.urls import path
from .views import welcome, generate_report


urlpatterns = [
    path('', welcome),
    path('generate-report/', generate_report, name='generate_report'),
]
