# Generated by Django 2.2.3 on 2019-07-29 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangolyteevents', '0007_event_organizer_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='organizer_description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
