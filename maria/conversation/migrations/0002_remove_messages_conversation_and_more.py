# Generated by Django 5.1.6 on 2025-02-21 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conversation', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='messages',
            name='conversation',
        ),
        migrations.RemoveField(
            model_name='messages',
            name='created_at',
        ),
        migrations.AddField(
            model_name='messages',
            name='topic',
            field=models.TextField(default='introduce yourself', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='messages',
            name='role',
            field=models.CharField(max_length=9),
        ),
        migrations.DeleteModel(
            name='Conversation',
        ),
    ]
