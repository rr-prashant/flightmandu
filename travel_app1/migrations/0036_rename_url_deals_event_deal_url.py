# Generated by Django 3.2.25 on 2024-04-29 05:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('travel_app1', '0035_deals_event_url'),
    ]

    operations = [
        migrations.RenameField(
            model_name='deals_event',
            old_name='url',
            new_name='deal_url',
        ),
    ]
