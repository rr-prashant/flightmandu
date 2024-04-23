# Generated by Django 5.0 on 2024-04-22 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel_app1', '0020_remove_package_location_desc_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='quotation_fill_Airlines',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hotels', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='quotation_fill_Hotels',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hotels', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='quotation_fill_Inclusion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inclusion', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='quotation_fill_Meals',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meals', models.TextField()),
            ],
        ),
    ]