# Generated by Django 5.1.3 on 2024-11-28 04:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('gender', models.CharField(choices=[('Male', '남성'), ('Female', '여성')], max_length=10)),
                ('phone_number', models.CharField(max_length=100)),
                ('address', models.CharField(blank=True, max_length=100, null=True)),
                ('key', models.CharField(default='000000', max_length=6)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
