# Generated by Django 3.2.1 on 2021-05-10 14:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('API_Quiz', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(max_length=300)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Quiz_Set', to='API_Quiz.quiz_details')),
            ],
        ),
    ]