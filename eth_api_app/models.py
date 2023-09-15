from django.db import models


class Wallet(models.Model):
    public_key = models.CharField(max_length=100)
    private_key = models.CharField(max_length=100)
