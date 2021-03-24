# Generated by Django 3.1.7 on 2021-03-23 18:51

from django.db import migrations


def null_zerolength(apps, schema_editor):
    Bearer = apps.get_model('radioepg', 'Bearer')
    for bearer in Bearer.objects.all():
        if bearer.frequency == '':
            bearer.frequency = None
            bearer.save()


class Migration(migrations.Migration):

    dependencies = [
        ('radioepg', '0017_auto_20210323_2046'),
    ]

    operations = [
        migrations.RunPython(null_zerolength),
    ]