# Generated by Django 2.0.5 on 2020-05-31 14:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Plots', '0003_plot_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plot',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rel_from_set', to=settings.AUTH_USER_MODEL),
        ),
    ]
