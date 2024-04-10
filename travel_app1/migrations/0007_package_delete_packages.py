# Generated by Django 5.0 on 2024-04-10 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel_app1', '0006_packages'),
    ]

    operations = [
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country_name', models.CharField(blank=True, max_length=200, null=True)),
                ('location_name', models.CharField(blank=True, max_length=200, null=True)),
                ('location_image', models.ImageField(blank=True, null=True, upload_to='packages_image')),
                ('location_desc', models.CharField(blank=True, max_length=200, null=True)),
                ('package_duration', models.IntegerField(blank=True, null=True)),
                ('total_person', models.IntegerField(blank=True, null=True)),
                ('accomodation', models.CharField(blank=True, max_length=200, null=True)),
                ('hotel_transfer', models.CharField(blank=True, max_length=200, null=True)),
                ('visa', models.CharField(blank=True, max_length=200, null=True)),
                ('meals', models.CharField(blank=True, max_length=200, null=True)),
                ('airfare', models.CharField(blank=True, max_length=200, null=True)),
                ('insurance_coverage', models.CharField(blank=True, max_length=200, null=True)),
                ('overview', models.TextField(blank=True, null=True)),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Packages',
        ),
    ]
