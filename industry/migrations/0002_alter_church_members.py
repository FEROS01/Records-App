# Generated by Django 5.1.2 on 2024-10-27 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('industry', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='church',
            name='members',
            field=models.ManyToManyField(blank=True, related_name='%(class)s_industry', to='industry.member'),
        ),
    ]