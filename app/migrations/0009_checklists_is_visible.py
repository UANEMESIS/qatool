# Generated by Django 2.0.5 on 2018-07-18 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20180718_1657'),
    ]

    operations = [
        migrations.AddField(
            model_name='checklists',
            name='is_visible',
            field=models.BooleanField(default=True),
        ),
    ]
