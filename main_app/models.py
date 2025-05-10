from django.db import models

# Create your models here.
class AdminDetails(models.Model):
    ROLE_CHOICES = [
        ('Accounts','Accounts and Finance'),
        ('Marketing','Marketing and Sales'),
        ('Delveloper','Delveloper or Technical'),
        ('CEO','Head or CEO'),
    ]
    name = models.CharField(max_length=2000)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    is_superAdmin = models.BooleanField(default=False)

    def __str__(self):
        return self.name