# Generated by Django 5.0.6 on 2024-06-13 15:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0012_productcategory'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ProductCategory',
        ),
    ]