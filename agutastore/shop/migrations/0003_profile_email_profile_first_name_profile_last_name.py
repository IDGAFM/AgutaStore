# Generated by Django 5.0.6 on 2024-05-30 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='email',
            field=models.EmailField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='profile',
            name='first_name',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name='profile',
            name='last_name',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]