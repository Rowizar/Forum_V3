# Generated by Django 5.0.3 on 2024-03-09 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qa_app', '0005_historicalquestion'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalquestion',
            name='is_closed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='question',
            name='is_closed',
            field=models.BooleanField(default=False),
        ),
    ]
