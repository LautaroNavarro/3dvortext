# Generated by Django 2.2.10 on 2020-02-16 02:27

from django.db import migrations, models
import django.db.models.deletion
import helpers.date_helpers
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('addresses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('lastname', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.EmailField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('status', models.IntegerField(default=0)),
                ('access_level', models.IntegerField(default=0)),
                ('mercado_pago_id', models.CharField(blank=True, max_length=255, null=True)),
                ('created', models.DateTimeField(default=helpers.date_helpers.get_current_utc_datetime)),
                ('changed', models.DateTimeField(default=helpers.date_helpers.get_current_utc_datetime)),
                ('addresses', models.ManyToManyField(blank=True, to='addresses.Address')),
            ],
        ),
        migrations.CreateModel(
            name='Confirmation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('verified', models.BooleanField(default=False)),
                ('created', models.DateTimeField()),
                ('changed', models.DateTimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.User')),
            ],
        ),
    ]
