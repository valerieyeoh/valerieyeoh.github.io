# Generated by Django 2.0 on 2020-01-04 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_auto_20200103_2236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='input_val_prod',
            field=models.CharField(default=[{'high-lt': '0.00', 'high-mt': '0.00', 'high-st': '0.00', 'low-lt': '0.00', 'low-mt': '0.00', 'low-st': '0.00', 'quality-prem': '0.00', 'transport-cost': '0.00'}, {'high-lt': '0.00', 'high-mt': '0.00', 'high-st': '0.00', 'low-lt': '0.00', 'low-mt': '0.00', 'low-st': '0.00', 'quality-prem': '0.00', 'transport-cost': '0.00'}, {'high-lt': '0.00', 'high-mt': '0.00', 'high-st': '0.00', 'low-lt': '0.00', 'low-mt': '0.00', 'low-st': '0.00', 'quality-prem': '0.00', 'transport-cost': '0.00'}, {'high-lt': '0.00', 'high-mt': '0.00', 'high-st': '0.00', 'low-lt': '0.00', 'low-mt': '0.00', 'low-st': '0.00', 'quality-prem': '0.00', 'transport-cost': '0.00'}, {'high-lt': '0.00', 'high-mt': '0.00', 'high-st': '0.00', 'low-lt': '0.00', 'low-mt': '0.00', 'low-st': '0.00', 'quality-prem': '0.00', 'transport-cost': '0.00'}, {'high-lt': '0.00', 'high-mt': '0.00', 'high-st': '0.00', 'low-lt': '0.00', 'low-mt': '0.00', 'low-st': '0.00', 'quality-prem': '0.00', 'transport-cost': '0.00'}], max_length=100, null=True),
        ),
    ]
