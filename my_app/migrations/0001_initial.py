# Generated by Django 4.2.1 on 2023-08-15 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icon', models.CharField(max_length=255, null=True)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
    ]
