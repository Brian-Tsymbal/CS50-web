# Generated by Django 3.0.8 on 2020-07-31 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_listings_priceint'),
    ]

    operations = [
        migrations.AddField(
            model_name='listings',
            name='Active',
            field=models.BooleanField(default=True),
        ),
    ]
