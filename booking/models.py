from django.db import models
from django.core.validators import RegexValidator

class Appointment(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")]
    )
    date = models.DateField()
    time_slot = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('date', 'time_slot')
    
    def __str__(self):
        return f"{self.name} - {self.date} {self.time_slot}"