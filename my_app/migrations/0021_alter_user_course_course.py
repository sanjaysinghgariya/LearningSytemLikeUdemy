# Generated by Django 4.2.1 on 2023-09-10 13:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0020_alter_user_course_course'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_course',
            name='course',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='my_app.course'),
        ),
    ]
