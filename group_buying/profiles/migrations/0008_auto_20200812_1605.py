# Generated by Django 2.1.5 on 2020-08-12 10:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0007_dealer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dealer',
            name='profile',
        ),
        migrations.RemoveField(
            model_name='dealer',
            name='user',
        ),
        migrations.DeleteModel(
            name='Dealer',
        ),
    ]
