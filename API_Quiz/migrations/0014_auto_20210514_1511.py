# Generated by Django 3.2.1 on 2021-05-14 15:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('API_Quiz', '0013_question_isopentext'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='submission',
            name='quiz_id',
        ),
        migrations.AddField(
            model_name='submission',
            name='question_id',
            field=models.ForeignKey(default=10, on_delete=django.db.models.deletion.CASCADE, related_name='Ques_Set', to='API_Quiz.question'),
            preserve_default=False,
        ),
    ]
