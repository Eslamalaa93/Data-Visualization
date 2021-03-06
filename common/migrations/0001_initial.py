# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-05 19:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DjangoMigrations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('applied', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_migrations',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DltOrderDetail',
            fields=[
                ('id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('customer_signature', models.DateField(blank=True, null=True)),
                ('first_lvo', models.DateField(blank=True, db_column='first_LVO', null=True)),
                ('last_lvo', models.DateField(blank=True, db_column='last_LVO', null=True)),
                ('gad', models.DateField(blank=True, db_column='GAD', null=True)),
                ('sio', models.DateField(blank=True, db_column='SIO', null=True)),
                ('gold_cr', models.DateField(blank=True, db_column='GOLD_CR', null=True)),
                ('srf', models.DateField(blank=True, db_column='SRF', null=True)),
                ('cso', models.DateField(blank=True, db_column='CSO', null=True)),
                ('cav', models.DateField(blank=True, db_column='CAV', null=True)),
                ('equipment_order', models.DateField(blank=True, null=True)),
                ('shipment_requested', models.DateField(blank=True, null=True)),
                ('shipment_date', models.DateField(blank=True, null=True)),
                ('equipment_delivery', models.DateField(blank=True, null=True)),
                ('install_order', models.DateField(blank=True, null=True)),
                ('install_request', models.DateField(blank=True, null=True)),
                ('at_completion', models.DateField(blank=True, db_column='AT_completion', null=True)),
                ('actual_install', models.DateField(blank=True, null=True)),
                ('sat_completion', models.DateField(blank=True, db_column='SAT_completion', null=True)),
                ('num_fields', models.IntegerField(blank=True, null=True)),
                ('cutdate', models.DateField(blank=True, db_column='CUTDate', null=True)),
                ('gold_ref', models.CharField(blank=True, db_column='Gold_ref', max_length=45, null=True)),
                ('customername', models.TextField(blank=True, db_column='CustomerName', null=True)),
                ('customercode', models.CharField(blank=True, db_column='CustomerCode', max_length=45, null=True)),
                ('country', models.CharField(blank=True, db_column='Country', max_length=45, null=True)),
                ('cmp_productname', models.CharField(blank=True, db_column='CMP_ProductName', max_length=45, null=True)),
                ('ldm_region', models.CharField(blank=True, db_column='LDM_region', max_length=45, null=True)),
                ('ldm_team', models.CharField(blank=True, db_column='LDM_team', max_length=45, null=True)),
                ('ldm', models.CharField(blank=True, db_column='LDM', max_length=45, null=True)),
                ('rfb', models.DateField(blank=True, db_column='RFB', null=True)),
                ('rfs', models.DateField(blank=True, db_column='RFS', null=True)),
                ('scn', models.DateField(blank=True, db_column='SCN', null=True)),
                ('status', models.CharField(blank=True, db_column='Status', max_length=45, null=True)),
                ('sdm', models.CharField(blank=True, db_column='SDM', max_length=45, null=True)),
                ('sdm_team', models.CharField(blank=True, db_column='SDM_Team', max_length=45, null=True)),
                ('sdm_msc', models.CharField(blank=True, db_column='SDM_MSC', max_length=45, null=True)),
                ('ltc', models.CharField(blank=True, db_column='LTC', max_length=45, null=True)),
                ('pocm', models.CharField(blank=True, db_column='POCM', max_length=45, null=True)),
                ('pocm_team', models.CharField(blank=True, db_column='POCM_Team', max_length=45, null=True)),
                ('pocm_msc', models.CharField(blank=True, db_column='POCM_MSC', max_length=45, null=True)),
            ],
            options={
                'db_table': 'dlt_order_detail',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DltOrderDays',
            fields=[
                ('id', models.ForeignKey(db_column='id', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='common.DltOrderDetail')),
                ('dlt1a', models.IntegerField(blank=True, null=True)),
                ('dlt1b1', models.IntegerField(blank=True, null=True)),
                ('dlt1b2', models.IntegerField(blank=True, null=True)),
                ('dlt1c', models.IntegerField(blank=True, null=True)),
                ('dlt2', models.IntegerField(blank=True, null=True)),
                ('dlt3a1', models.IntegerField(blank=True, null=True)),
                ('dlt3a2', models.IntegerField(blank=True, null=True)),
                ('dlt3b1', models.IntegerField(blank=True, null=True)),
                ('dlt3b2', models.IntegerField(blank=True, null=True)),
                ('dlt3b3', models.IntegerField(blank=True, null=True)),
                ('dlt3b4', models.IntegerField(blank=True, null=True)),
                ('dlt3d', models.IntegerField(blank=True, null=True)),
                ('dlt3e', models.IntegerField(blank=True, null=True)),
                ('dlt4a', models.IntegerField(blank=True, null=True)),
                ('dlt4b', models.IntegerField(blank=True, null=True)),
                ('cutdate', models.DateField(blank=True, db_column='CUTDate', null=True)),
            ],
            options={
                'db_table': 'dlt_order_days',
                'managed': False,
            },
        ),
    ]
