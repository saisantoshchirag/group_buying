# Generated by Django 2.1.5 on 2020-08-29 03:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orders',
            name='address',
        ),
        migrations.RemoveField(
            model_name='orders',
            name='city',
        ),
        migrations.RemoveField(
            model_name='orders',
            name='email',
        ),
        migrations.RemoveField(
            model_name='orders',
            name='items_json',
        ),
        migrations.RemoveField(
            model_name='orders',
            name='name',
        ),
        migrations.RemoveField(
            model_name='orders',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='orders',
            name='state',
        ),
        migrations.RemoveField(
            model_name='orders',
            name='zip_code',
        ),
    ]