# Generated by Django 3.2.6 on 2021-08-22 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_userfollowing_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_pic',
            field=models.ImageField(blank=True, default='images/user_default.png', null=True, upload_to=''),
        ),
    ]
