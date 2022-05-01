# Generated by Django 4.0.3 on 2022-05-01 22:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='rating',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='vendor',
            name='rating_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='vendordetails',
            name='business_description',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vendordetails',
            name='closing_hours',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='vendordetails',
            name='latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='vendordetails',
            name='longitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='vendordetails',
            name='opening_hours',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='vendordetails',
            name='business_picture',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]