# Generated by Django 4.2.1 on 2023-09-18 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0034_contactus'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactus',
            name='Message',
            field=models.TextField(null=True),
        ),
    ]
