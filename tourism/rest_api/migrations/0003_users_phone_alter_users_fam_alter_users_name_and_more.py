# Generated by Django 4.1.1 on 2022-09-30 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest_api', '0002_alter_perevaladded_connect_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='phone',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='fam',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='name',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='otc',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
