# Generated by Django 2.0.5 on 2018-07-18 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_remove_actions_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actions',
            name='date_end',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='actions',
            name='notes',
            field=models.TextField(blank=True, max_length=1500, null=True),
        ),
        migrations.AlterField(
            model_name='checklists',
            name='notes',
            field=models.TextField(blank=True, max_length=1500, null=True),
        ),
    ]
