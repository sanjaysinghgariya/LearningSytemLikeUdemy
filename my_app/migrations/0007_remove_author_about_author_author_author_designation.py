# Generated by Django 4.2.1 on 2023-09-05 04:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0006_lesson_video'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='about_author',
        ),
        migrations.AddField(
            model_name='author',
            name='author_designation',
            field=models.CharField(max_length=255, null=True),
        ),
    ]