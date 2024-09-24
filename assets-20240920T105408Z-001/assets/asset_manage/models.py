from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class Assets(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    asset_name= models.CharField(max_length=50)
    price=models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    purchase_date=models.DateTimeField(auto_now_add=True)
    purchased=models.BooleanField(default=False)

class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    username = models.CharField(max_length=50, unique=True)
    asset_assigned = models.ForeignKey(Assets, on_delete=models.CASCADE, related_name='asset', blank=True, null=True)

    def __str__(self):
        return {self.username}