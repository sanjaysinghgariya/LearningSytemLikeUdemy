# Generated by Django 4.2.1 on 2023-09-10 12:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0018_remove_user_course_courses_user_course_course'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_course',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_app.course'),
        ),
    ]
