# Generated by Django 4.1.5 on 2023-03-29 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0029_alter_commericalimage_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commerical',
            name='publisher',
            field=models.CharField(blank=True, choices=[('همه', 'همه'), ('شخصی', 'شخصی'), ('املاک', 'املاک')], default='همه', max_length=200, null=True),
        ),
    ]