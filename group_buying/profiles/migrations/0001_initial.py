# Generated by Django 2.1.5 on 2020-08-27 09:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('chat', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ChangePassword',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.IntegerField()),
                ('code', models.IntegerField()),
                ('date', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.IntegerField(default=0)),
                ('image', models.ImageField(blank=True, default='prof1.jpeg', upload_to='profile_image')),
                ('gender', models.CharField(max_length=10)),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
                ('pincode', models.IntegerField(default=0)),
                ('is_dealer', models.BooleanField(default=False, verbose_name='dealer status')),
                ('is_user', models.BooleanField(default=True, verbose_name='user status')),
                ('is_admin', models.BooleanField(default=False, verbose_name='admin status')),
                ('is_subscribed', models.BooleanField(default=False, verbose_name='subscription status')),
                ('room', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='chat.ChatRoom')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
