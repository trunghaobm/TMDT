# Generated by Django 4.1.3 on 2022-11-19 12:05

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('GDNusers', '0007_alter_delivery_method_alter_delivery_pay_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pay',
            name='date',
            field=models.DateField(blank=True, default=django.utils.timezone.now, null=True),
        ),
    ]