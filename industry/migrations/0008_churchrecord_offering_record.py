# Generated by Django 5.1.2 on 2024-10-27 15:51

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('industry', '0007_remove_offering_record_delete_churchrecord'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChurchRecord',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('sermon_title', models.TextField()),
                ('text', models.CharField(max_length=200)),
                ('service_date', models.DateTimeField(auto_now_add=True)),
                ('edit_date', models.DateTimeField(auto_now=True)),
                ('church', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='church_record', to='industry.church')),
                ('service', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='service_record', to='industry.service')),
            ],
        ),
        migrations.AddField(
            model_name='offering',
            name='record',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='offering', to='industry.churchrecord'),
        ),
    ]