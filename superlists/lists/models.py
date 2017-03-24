from django.db import models

1
class Item(models.Model):
    text = models.TextField(default='')
