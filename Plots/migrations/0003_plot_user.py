# Generated by Django 2.0.5 on 2020-05-31 14:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Plots', '0002_auto_20200531_1540'),
    ]

    operations = [
        migrations.AddField(
            model_name='plot',
            name='user',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='rel_from_set', to=settings.AUTH_USER_MODEL),
        ),
    ]
