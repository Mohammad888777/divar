# Generated by Django 4.1.5 on 2023-03-17 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_commerical_publisherforcar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commerical',
            name='phone_status',
            field=models.CharField(blank=True, choices=[('همه', 'همه'), ('نو', 'نو'), ('در حد نو', 'در حد نو'), ('کارکرده', 'کارکرده')], max_length=100, null=True),
        ),
    ]