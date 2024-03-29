# Generated by Django 2.0 on 2019-12-19 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20191217_0157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='bounds',
            field=models.CharField(default='', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='session',
            name='gross_margin',
            field=models.CharField(default='', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='session',
            name='gross_margins',
            field=models.CharField(default='', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='session',
            name='hourly_labor_cost',
            field=models.CharField(default='', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='session',
            name='labor_hours_avail',
            field=models.CharField(default='', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='session',
            name='product',
            field=models.CharField(default='', max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='session',
            name='product_1',
            field=models.CharField(default='', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='session',
            name='product_2',
            field=models.CharField(default='', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='session',
            name='product_3',
            field=models.CharField(default='', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='session',
            name='raw_material',
            field=models.CharField(default='', max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='session',
            name='result',
            field=models.CharField(default='', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='session',
            name='sector_req',
            field=models.CharField(default='', max_length=100, null=True),
        ),
    ]
