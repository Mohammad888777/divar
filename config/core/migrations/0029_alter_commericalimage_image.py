# Generated by Django 4.1.5 on 2023-03-29 11:01

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0028_commerical_salary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commericalimage',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg'])]),
        ),
    ]
