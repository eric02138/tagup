# Generated by Django 2.1.3 on 2018-12-02 18:19

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('record', '0002_record_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='createdDate',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='record',
            name='lastModificationDate',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='record',
            name='value1',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='record',
            name='value2',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='record',
            name='value3',
            field=models.IntegerField(default=0),
        ),
    ]
