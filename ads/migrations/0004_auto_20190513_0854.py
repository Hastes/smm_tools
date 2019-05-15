# Generated by Django 2.2.1 on 2019-05-13 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0003_auto_20190513_0650'),
    ]

    operations = [
        migrations.AddField(
            model_name='ads',
            name='facebook_loaded',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='ads',
            name='vk_loaded',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='facebook_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='vk_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
