# Generated by Django 4.1.5 on 2023-03-10 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='location_nickName',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]