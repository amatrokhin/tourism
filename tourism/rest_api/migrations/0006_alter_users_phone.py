# Generated by Django 4.1.1 on 2022-09-30 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest_api', '0005_alter_coords_height_alter_coords_latitude_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='phone',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
