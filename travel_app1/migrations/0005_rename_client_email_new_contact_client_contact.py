# Generated by Django 5.0 on 2024-04-07 17:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('travel_app1', '0004_visa_service_countries'),
    ]

    operations = [
        migrations.RenameField(
            model_name='new_contact',
            old_name='client_email',
            new_name='client_contact',
        ),
    ]
