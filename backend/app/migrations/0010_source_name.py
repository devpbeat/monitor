# Generated by Django 3.2.6 on 2022-05-09 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_alter_updates_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='source',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
