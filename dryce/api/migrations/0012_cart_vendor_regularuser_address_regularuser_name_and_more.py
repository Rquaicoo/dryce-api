# Generated by Django 4.0.3 on 2022-06-01 08:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0005_rename_business_certificate_vendordetails_certificate_and_more'),
        ('api', '0011_rename_blazers_cart_cardigans_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='vendor',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='vendor.vendor'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='regularuser',
            name='address',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='regularuser',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='regularuser',
            name='phone',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cost', models.IntegerField(blank=True, null=True)),
                ('payment_method', models.CharField(blank=True, max_length=15, null=True)),
                ('delivery', models.CharField(blank=True, max_length=50, null=True)),
                ('cart', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.cart')),
            ],
        ),
    ]