# Generated by Django 4.2.1 on 2023-09-10 13:49

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('my_app', '0023_delete_user_course'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='User_Course1',
            new_name='User_Course',
        ),
    ]
