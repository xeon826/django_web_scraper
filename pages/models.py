from django.db import models
from django.conf import settings


class ItemStatus(models.Model):
    title = models.CharField(max_length=50, unique=True, blank=True)

    def __str__(self):
        return self.title


class Item(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    url = models.CharField(max_length=200, null=True, blank=True)
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL,
                                    null=True,
                                    blank=True,
                                    on_delete=models.PROTECT)
    status = models.ForeignKey(ItemStatus,
                               to_field='title',
                               default='Unprocessed',
                               on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def is_processed(self):
        return True if self.status.title == 'Processed' else False