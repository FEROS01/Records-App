# Generated by Django 5.1.2 on 2024-10-27 14:58

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('industry', '0002_alter_church_members'),
    ]

    operations = [
        migrations.AlterField(
            model_name='church',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
