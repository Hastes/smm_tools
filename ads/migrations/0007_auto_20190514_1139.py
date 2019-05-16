# Generated by Django 2.2.1 on 2019-05-14 11:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ads', '0006_auto_20190514_1102'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ads',
            name='vk_loaded',
            field=models.BooleanField(default=False),
        ),
    ]