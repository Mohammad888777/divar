# Generated by Django 4.1.5 on 2023-03-10 16:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_commerical_smallcity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commerical',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.location'),
        ),
    ]
