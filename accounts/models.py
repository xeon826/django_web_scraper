from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    gis_validation = models.BooleanField(null=True, blank=True, default=False)
    items_per_grid = models.IntegerField(null=True, blank=True, default=20)

    def __str__(self):
        return self.email