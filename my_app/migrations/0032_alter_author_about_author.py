# Generated by Django 4.2.1 on 2023-09-11 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0031_alter_categories_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='about_author',
            field=models.CharField(max_length=2555, null=True),
        ),
    ]
