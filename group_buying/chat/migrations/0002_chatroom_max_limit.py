# Generated by Django 3.0.1 on 2020-08-27 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatroom',
            name='max_limit',
            field=models.IntegerField(default=10),
            preserve_default=False,
        ),
    ]