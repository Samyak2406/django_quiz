# Generated by Django 3.2.1 on 2021-05-10 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API_Quiz', '0003_answer'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz_details',
            name='quiz_end',
            field=models.IntegerField(default=1234567),
            preserve_default=False,
        ),
    ]
