# Generated by Django 2.0 on 2020-01-03 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20200103_1306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='input_val_rm',
            field=models.CharField(default=[], max_length=100, null=True),
        ),
    ]