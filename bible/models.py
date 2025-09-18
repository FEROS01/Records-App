# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class SMeta(models.Model):
    field = models.CharField(primary_key=True)
    value = models.TextField(blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'meta'

class Verses(models.Model):
    book = models.IntegerField(primary_key=True)
    chapter = models.IntegerField()
    verse = models.IntegerField()
    text = models.TextField()

    class Meta:
        managed = False
        db_table = 'verses'