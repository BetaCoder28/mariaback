# Generated by Django 5.1.6 on 2025-03-01 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conversation', '0006_feedback'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='conversation_id',
            field=models.CharField(default='default_conversation', max_length=100),
        ),
    ]
