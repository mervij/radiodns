# Generated by Django 3.1.7 on 2021-03-10 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('radioepg', '0010_auto_20210228_1616'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageSlide',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trigger_time', models.DateTimeField()),
                ('url', models.CharField(max_length=512)),
                ('sent', models.BooleanField()),
            ],
        ),
    ]
