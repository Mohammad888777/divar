# Generated by Django 4.1.5 on 2023-03-15 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_alter_commerical_rent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commerical',
            name='rent',
            field=models.IntegerField(blank=True, choices=[('کامل', 'کامل'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('7', '7')], null=True),
        ),
    ]
