# Generated by Django 4.2.1 on 2023-09-10 14:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0028_rename_course_user_course_course'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user_course',
            name='Course',
        ),
        migrations.AddField(
            model_name='user_course',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='my_app.course'),
        ),
    ]