from django.db import models

# Create your models here.
class dp(models.Model):
    id = models.AutoField
    profilepic = models.ImageField(null=True, upload_to="Profile_Pics")
    email = models.EmailField(unique=True, default="example@gmail.com")

    def __str__(self):
        return self.email