# Generated by Django 4.1.5 on 2023-03-04 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='commerical',
            name='rent',
            field=models.IntegerField(blank=True, choices=[('کامل', 'کامل'), (5000000, 5000000), (10000000, 10000000), (15000000, 15000000), (20000000, 20000000), (25000000, 25000000), (30000000, 30000000), (35000000, 35000000), (40000000, 40000000), (45000000, 45000000), (50000000, 50000000)], null=True),
        ),
        migrations.AddField(
            model_name='commerical',
            name='vadieh',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
