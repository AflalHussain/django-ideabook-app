# Generated by Django 3.2.6 on 2021-08-17 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ideabook', '0011_alter_idea_idea_edit_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='idea',
            name='idea_edit_date',
            field=models.DateTimeField(default=None, null=True, verbose_name='date idea edited'),
        ),
    ]