# Generated by Django 3.2 on 2021-04-27 10:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('radiovis', '0007_auto_20210422_1424'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imageslide',
            name='image',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='radiovis.image'),
        ),
    ]
