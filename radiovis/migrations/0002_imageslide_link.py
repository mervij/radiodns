# Generated by Django 3.1.7 on 2021-03-22 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('radiovis', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='imageslide',
            name='link',
            field=models.CharField(blank=True, max_length=2000),
        ),
    ]
