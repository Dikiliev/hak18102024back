# Generated by Django 5.0.4 on 2024-10-19 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_user_signature'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='signature',
            field=models.TextField(blank=True, null=True),
        ),
    ]
