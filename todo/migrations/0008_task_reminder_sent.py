# Generated by Django 5.1.1 on 2024-11-12 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0007_alter_task_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='reminder_sent',
            field=models.BooleanField(default=False),
        ),
    ]