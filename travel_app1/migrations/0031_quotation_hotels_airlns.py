# Generated by Django 5.0 on 2024-04-24 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel_app1', '0030_quotation_num_adult_quotation_num_child_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='quotation_hotels',
            name='airlns',
            field=models.TextField(blank=True, null=True),
        ),
    ]