# Generated by Django 2.2.10 on 2020-02-16 02:34

from django.db import migrations, models
import helpers.date_helpers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=2048)),
                ('price_per_kilogram', models.CharField(max_length=255)),
                ('changed', models.DateTimeField(default=helpers.date_helpers.get_current_utc_datetime)),
                ('created', models.DateTimeField(default=helpers.date_helpers.get_current_utc_datetime)),
            ],
        ),
    ]
