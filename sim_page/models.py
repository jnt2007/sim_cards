from __future__ import unicode_literals

from django.db import models

# Create your models here.


class SimCard(models.Model):

    sim_number = models.IntegerField(blank=False)
    name = models.CharField(max_length=30, blank=False)
    owner = models.ForeignKey('sim_page.SIMOwner', blank=False)
    cell_operator = models.ForeignKey('sim_page.MobileOperator', blank=False)
    tariff = models.CharField(max_length=30, blank=False)
    # apn = models.CharField(max_length=30, blank=True, null=True)
    balance = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    last_update = models.DateTimeField(blank=True, null=True)
    appointment = models.CharField(max_length=40, blank=False)
    comment = models.CharField(max_length=40, blank=True, null=True)
    # login = models.CharField(max_length=30, blank=False)
    password = models.CharField(max_length=30, blank=False)
    balance_renewal_in_progress = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class MobileOperator(models.Model):

    operator = models.CharField(max_length=30, blank=False)

    def __str__(self):
        return self.operator


class SIMOwner(models.Model):

    owner = models.CharField(max_length=30, blank=False)

    def __str__(self):
        return self.owner