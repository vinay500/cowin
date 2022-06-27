from django.db import models
from CPD_app.models import *
# Create your models here.
class SlotBook(models.Model):
    aadhaar=models.ForeignKey(Users,on_delete=models.CASCADE,null=True)
    state=models.CharField(max_length=15)
    district=models.CharField(max_length=15)
    vaccine=models.CharField(max_length=15)
    slot=models.DateField()

    def __str__(self):
        return self.state

