# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DltOrderDays(models.Model):
    id = models.ForeignKey('DltOrderDetail', models.DO_NOTHING, db_column='id', primary_key=True)
    dlt1a = models.IntegerField(blank=True, null=True)
    dlt1b1 = models.IntegerField(blank=True, null=True)
    dlt1b2 = models.IntegerField(blank=True, null=True)
    dlt1c = models.IntegerField(blank=True, null=True)
    dlt2 = models.IntegerField(blank=True, null=True)
    dlt3a1 = models.IntegerField(blank=True, null=True)
    dlt3a2 = models.IntegerField(blank=True, null=True)
    dlt3b1 = models.IntegerField(blank=True, null=True)
    dlt3b2 = models.IntegerField(blank=True, null=True)
    dlt3b3 = models.IntegerField(blank=True, null=True)
    dlt3b4 = models.IntegerField(blank=True, null=True)
    dlt3d = models.IntegerField(blank=True, null=True)
    dlt3e = models.IntegerField(blank=True, null=True)
    dlt4a = models.IntegerField(blank=True, null=True)
    dlt4b = models.IntegerField(blank=True, null=True)
    cutdate = models.DateField(db_column='CUTDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'dlt_order_days'


class DltOrderDetail(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    customer_signature = models.DateField(blank=True, null=True)
    first_lvo = models.DateField(db_column='first_LVO', blank=True, null=True)  # Field name made lowercase.
    last_lvo = models.DateField(db_column='last_LVO', blank=True, null=True)  # Field name made lowercase.
    gad = models.DateField(db_column='GAD', blank=True, null=True)  # Field name made lowercase.
    sio = models.DateField(db_column='SIO', blank=True, null=True)  # Field name made lowercase.
    gold_cr = models.DateField(db_column='GOLD_CR', blank=True, null=True)  # Field name made lowercase.
    srf = models.DateField(db_column='SRF', blank=True, null=True)  # Field name made lowercase.
    cso = models.DateField(db_column='CSO', blank=True, null=True)  # Field name made lowercase.
    cav = models.DateField(db_column='CAV', blank=True, null=True)  # Field name made lowercase.
    equipment_order = models.DateField(blank=True, null=True)
    shipment_requested = models.DateField(blank=True, null=True)
    shipment_date = models.DateField(blank=True, null=True)
    equipment_delivery = models.DateField(blank=True, null=True)
    install_order = models.DateField(blank=True, null=True)
    install_request = models.DateField(blank=True, null=True)
    at_completion = models.DateField(db_column='AT_completion', blank=True, null=True)  # Field name made lowercase.
    actual_install = models.DateField(blank=True, null=True)
    sat_completion = models.DateField(db_column='SAT_completion', blank=True, null=True)  # Field name made lowercase.
    num_fields = models.IntegerField(blank=True, null=True)
    cutdate = models.DateField(db_column='CUTDate', blank=True, null=True)  # Field name made lowercase.
    gold_ref = models.CharField(db_column='Gold_ref', max_length=45, blank=True, null=True)  # Field name made lowercase.
    customername = models.TextField(db_column='CustomerName', blank=True, null=True)  # Field name made lowercase.
    customercode = models.CharField(db_column='CustomerCode', max_length=45, blank=True, null=True)  # Field name made lowercase.
    country = models.CharField(db_column='Country', max_length=45, blank=True, null=True)  # Field name made lowercase.
    cmp_productname = models.CharField(db_column='CMP_ProductName', max_length=45, blank=True, null=True)  # Field name made lowercase.
    ldm_region = models.CharField(db_column='LDM_region', max_length=45, blank=True, null=True)  # Field name made lowercase.
    ldm_team = models.CharField(db_column='LDM_team', max_length=45, blank=True, null=True)  # Field name made lowercase.
    ldm = models.CharField(db_column='LDM', max_length=45, blank=True, null=True)  # Field name made lowercase.
    rfb = models.DateField(db_column='RFB', blank=True, null=True)  # Field name made lowercase.
    rfs = models.DateField(db_column='RFS', blank=True, null=True)  # Field name made lowercase.
    scn = models.DateField(db_column='SCN', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=45, blank=True, null=True)  # Field name made lowercase.
    sdm = models.CharField(db_column='SDM', max_length=45, blank=True, null=True)  # Field name made lowercase.
    sdm_team = models.CharField(db_column='SDM_Team', max_length=45, blank=True, null=True)  # Field name made lowercase.
    sdm_msc = models.CharField(db_column='SDM_MSC', max_length=45, blank=True, null=True)  # Field name made lowercase.
    ltc = models.CharField(db_column='LTC', max_length=45, blank=True, null=True)  # Field name made lowercase.
    pocm = models.CharField(db_column='POCM', max_length=45, blank=True, null=True)  # Field name made lowercase.
    pocm_team = models.CharField(db_column='POCM_Team', max_length=45, blank=True, null=True)  # Field name made lowercase.
    pocm_msc = models.CharField(db_column='POCM_MSC', max_length=45, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'dlt_order_detail'

