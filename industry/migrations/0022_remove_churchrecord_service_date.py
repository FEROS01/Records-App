# Generated by Django 5.1.2 on 2025-04-05 13:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('industry', '0021_alter_churchrecord_service_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='churchrecord',
            name='service_date',
        ),
    ]
