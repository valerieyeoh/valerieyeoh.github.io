# Generated by Django 2.0 on 2019-12-16 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Temp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_id', models.CharField(default='', max_length=25)),
                ('product', models.CharField(default='', max_length=25)),
            ],
        ),
        migrations.DeleteModel(
            name='Session',
        ),
    ]
