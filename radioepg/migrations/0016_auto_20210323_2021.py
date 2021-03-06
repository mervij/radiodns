# Generated by Django 3.1.7 on 2021-03-23 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('radioepg', '0015_delete_imageslide'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bearer',
            old_name='mime_value',
            new_name='mimeValue',
        ),
        migrations.RenameField(
            model_name='service',
            old_name='medium_name',
            new_name='mediumName',
        ),
        migrations.RenameField(
            model_name='service',
            old_name='service_identifier',
            new_name='serviceIdentifier',
        ),
        migrations.RenameField(
            model_name='service',
            old_name='short_description',
            new_name='shortDescription',
        ),
        migrations.RenameField(
            model_name='service',
            old_name='short_name',
            new_name='shortName',
        ),
        migrations.RemoveField(
            model_name='bearer',
            name='bearer_id',
        ),
        migrations.AddField(
            model_name='bearer',
            name='bitrate',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='bearer',
            name='ecc',
            field=models.CharField(blank=True, max_length=2),
        ),
        migrations.AddField(
            model_name='bearer',
            name='frequency',
            field=models.CharField(blank=True, max_length=5),
        ),
        migrations.AddField(
            model_name='bearer',
            name='pi',
            field=models.CharField(blank=True, max_length=4),
        ),
        migrations.AddField(
            model_name='bearer',
            name='platform',
            field=models.CharField(blank=True, max_length=2),
        ),
        migrations.AddField(
            model_name='bearer',
            name='url',
            field=models.CharField(blank=True, max_length=2000),
        ),
        migrations.AlterField(
            model_name='bearer',
            name='cost',
            field=models.IntegerField(default=30),
        ),
    ]
