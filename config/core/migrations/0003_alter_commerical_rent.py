# Generated by Django 4.1.5 on 2023-03-04 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_commerical_rent_commerical_vadieh'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commerical',
            name='rent',
            field=models.CharField(blank=True, choices=[('کامل', 'کامل'), ('1000000', '1000000'), ('1500000', '1500000'), ('2000000', '2000000'), ('2500000', '2500000'), ('3000000', '3000000'), ('3500000', '3500000'), ('4000000', '4000000')], max_length=100, null=True),
        ),
    ]