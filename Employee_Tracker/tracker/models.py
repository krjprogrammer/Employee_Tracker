from django.db import models
from django.utils import timezone

class user_data(models.Model):
    first_name = models.CharField(max_length=255,null=True, blank=True)
    last_name = models.CharField(max_length=255,null=True, blank=True)
    username = models.CharField(max_length=255,null=True, blank=True)
    email_id = models.CharField(max_length=255,null=True, blank=True)
    password = models.CharField(max_length=255,null=True, blank=True)
    confirm_password = models.CharField(max_length=255,null=True, blank=True)
    mobile_number = models.CharField(max_length=255,null=True, blank=True)

class employee_details(models.Model):
    employee_id = models.CharField(max_length=255,null=True, blank=True)
    employee_first_name = models.CharField(max_length=255,null=True, blank=True)
    employee_last_name = models.CharField(max_length=255,null=True, blank=True)
    employee_email_id = models.CharField(max_length=255,null=True, blank=True)
    employee_mobile_number = models.CharField(max_length=255,null=True, blank=True)
    employee_image_encodeing = models.TextField(null=True)
    employee_account_number = models.CharField(max_length=255,null=True, blank=True)
    employee_bank = models.CharField(max_length=255,null=True, blank=True)
    employee_bank_ifsc_code = models.CharField(max_length=255,null=True, blank=True)

class mark_attendance_report(models.Model):
    employee_id = models.CharField(max_length=255,null=True, blank=True)
    employee_photo = models.BinaryField(null=True)
    date = models.DateField(default=timezone.now)
    time = models.TimeField(default=timezone.now)
    mark = models.BooleanField(default=False)

class GeofencedArea(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    radius = models.FloatField(help_text="Radius in meters")
