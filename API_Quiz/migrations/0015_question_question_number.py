# Generated by Django 3.2.1 on 2021-05-14 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API_Quiz', '0014_auto_20210514_1511'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='question_number',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
