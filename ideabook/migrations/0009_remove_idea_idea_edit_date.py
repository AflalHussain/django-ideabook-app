# Generated by Django 3.2.6 on 2021-08-17 08:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ideabook', '0008_idea_idea_edit_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='idea',
            name='idea_edit_date',
        ),
    ]
