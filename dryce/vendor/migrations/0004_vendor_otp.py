# Generated by Django 4.0.3 on 2022-05-24 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0003_rename_location_vendordetails_address_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='otp',
            field=models.CharField(blank=True, max_length=4, null=True),
        ),
    ]