# Generated by Django 4.2.1 on 2023-09-22 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0038_alter_comment_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='rating',
            field=models.CharField(choices=[('Below Average', 'Below Average'), ('Partly Average', 'Partly Average'), ('Average', 'Average'), ('Very Good', 'Very Good'), ('Excellent', 'Excellent')], max_length=100, null=True),
        ),
    ]
