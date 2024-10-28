# Generated by Django 5.1.2 on 2024-10-27 14:43

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('position', models.CharField()),
            ],
        ),
        migrations.CreateModel(
            name='Church',
            fields=[
                ('name', models.CharField(unique=True, verbose_name='industry_name')),
                ('owner', models.CharField(max_length=200)),
                ('uuid', models.UUIDField(editable=False, primary_key=True, serialize=False)),
                ('head_pastor', models.CharField(max_length=300, verbose_name="pastor's_name")),
                ('managers', models.ManyToManyField(related_name='%(class)s_industry', to=settings.AUTH_USER_MODEL)),
                ('members', models.ManyToManyField(related_name='%(class)s_industry', to='industry.member')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ChurchRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_name', models.TextField()),
                ('sermon_title', models.TextField()),
                ('text', models.CharField(max_length=200)),
                ('service_date', models.DateTimeField(auto_now_add=True)),
                ('edit_date', models.DateTimeField(auto_now=True)),
                ('church', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='industry.church')),
            ],
        ),
        migrations.CreateModel(
            name='Offering',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currency', models.CharField(max_length=100)),
                ('denomination', models.DecimalField(decimal_places=2, max_digits=6)),
                ('frequency', models.PositiveIntegerField(default=0)),
                ('record', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='offering', to='industry.churchrecord')),
            ],
        ),
    ]
