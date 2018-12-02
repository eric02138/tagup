from django.db import models

class Record(models.Model):
    _id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    value1 = models.IntegerField(default=0, null=False)
    value2 = models.IntegerField(default=0, null=False)
    value3 = models.IntegerField(default=0, null=False)
    createdDate = models.DateTimeField(auto_now_add=True)
    lastModificationDate = models.DateTimeField(auto_now_add=True)
