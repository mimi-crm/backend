# Generated by Django 5.1.3 on 2024-11-28 04:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("counsels", "0001_initial"),
        ("customers", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="counsel",
            name="customer",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="customers.customer"
            ),
        ),
    ]
