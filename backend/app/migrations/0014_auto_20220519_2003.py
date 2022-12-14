# Generated by Django 3.2.6 on 2022-05-19 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_auto_20220518_1921'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='metric_data',
            options={'verbose_name': 'Metric Data', 'verbose_name_plural': 'Metrics Data'},
        ),
        migrations.RenameField(
            model_name='metric',
            old_name='source',
            new_name='binded_source',
        ),
        migrations.AddField(
            model_name='metric',
            name='resource_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
