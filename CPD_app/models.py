from django.db import models

# Create your models here.
class Users(models.Model):
    photo_id_proof = models.CharField(max_length=30)
    aadhaar_number = models.CharField(primary_key=True,max_length=12)
    name=models.CharField(max_length=30)
    year_of_birth=models.IntegerField()
    gender=models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Otp(models.Model):
    # aadhaar=models.OneToOneField(Users,on_delete=models.CASCADE)
    mobile=models.CharField(max_length=10)
    otp=models.CharField(max_length=4)

    def __str__(self):
        return self.mobile