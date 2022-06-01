# Generated by Django 4.0.3 on 2022-05-24 10:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_contact_vendorchat_cart'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='blazers',
            new_name='cardigans',
        ),
        migrations.RenameField(
            model_name='cart',
            old_name='jackets',
            new_name='dress',
        ),
        migrations.RenameField(
            model_name='cart',
            old_name='siglets',
            new_name='shirts',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='skirts',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='suits',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='ties',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='tshirts',
        ),
    ]