# Generated by Django 5.0 on 2024-04-22 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel_app1', '0021_quotation_fill_airlines_quotation_fill_hotels_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='quotation_fill_Itinerary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('itinerary', models.TextField()),
            ],
        ),
        migrations.RenameField(
            model_name='quotation_fill_airlines',
            old_name='hotels',
            new_name='airlines',
        ),
    ]