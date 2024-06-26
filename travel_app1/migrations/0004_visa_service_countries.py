# Generated by Django 5.0 on 2024-04-07 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel_app1', '0003_flight_request_adult_flight_request_children_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Visa_Service_Countries',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country_name', models.CharField(blank=True, max_length=200, null=True)),
                ('country_flag', models.ImageField(blank=True, null=True, upload_to='country_flag')),
            ],
        ),
    ]
