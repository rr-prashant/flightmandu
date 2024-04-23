# Generated by Django 5.0 on 2024-04-17 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel_app1', '0014_company_members'),
    ]

    operations = [
        migrations.AddField(
            model_name='company_members',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='company_members',
            name='is_member',
            field=models.BooleanField(default=False),
        ),
    ]
