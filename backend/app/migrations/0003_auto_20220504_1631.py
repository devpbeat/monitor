# Generated by Django 3.2.6 on 2022-05-04 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20220504_1625'),
    ]

    operations = [
        migrations.AlterField(
            model_name='credentials',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='credentials',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
