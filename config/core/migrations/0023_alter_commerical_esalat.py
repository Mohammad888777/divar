# Generated by Django 4.1.5 on 2023-03-22 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_commerical_anbari_commerical_cloths_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commerical',
            name='esalat',
            field=models.CharField(blank=True, choices=[('همه', 'همه'), ('اصل', 'اصل'), ('تقلبی', 'تقلبی')], default='همه', max_length=100, null=True),
        ),
    ]
