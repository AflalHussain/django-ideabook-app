# Generated by Django 3.2.6 on 2021-08-17 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ideabook', '0009_remove_idea_idea_edit_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='idea',
            name='idea_edit_date',
            field=models.DateTimeField(blank=True, default=None, verbose_name='date idea edited'),
        ),
    ]
