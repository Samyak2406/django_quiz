# Generated by Django 3.2.1 on 2021-05-11 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API_Quiz', '0006_quiz_details_submission'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz_details',
            name='submission',
            field=models.CharField(blank=True, max_length=100000),
        ),
    ]