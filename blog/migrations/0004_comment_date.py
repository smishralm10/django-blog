# Generated by Django 3.1.1 on 2020-11-24 14:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20201124_1229'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]