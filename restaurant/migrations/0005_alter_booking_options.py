# Generated by Django 5.0.7 on 2024-07-29 21:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0004_alter_booking_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='booking',
            options={'ordering': ['reservation_date', 'reservation_slot']},
        ),
    ]
