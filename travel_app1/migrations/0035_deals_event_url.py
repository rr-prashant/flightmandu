# Generated by Django 3.2.25 on 2024-04-29 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel_app1', '0034_package_is_featured'),
    ]

    operations = [
        migrations.AddField(
            model_name='deals_event',
            name='url',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
