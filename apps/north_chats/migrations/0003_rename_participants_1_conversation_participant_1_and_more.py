# Generated by Django 5.1 on 2025-01-15 22:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('north_chats', '0002_remove_conversation_participants_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='conversation',
            old_name='participants_1',
            new_name='participant_1',
        ),
        migrations.RenameField(
            model_name='conversation',
            old_name='participants_2',
            new_name='participant_2',
        ),
    ]
