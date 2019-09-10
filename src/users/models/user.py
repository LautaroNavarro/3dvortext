from django.db import models


class User(models.Model):

    name = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    mercado_pago_id = models.CharField(max_length=255)
    created = models.DateTimeField()
    changed = models.DateTimeField()
