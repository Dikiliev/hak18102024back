# Generated by Django 5.1.2 on 2024-10-19 02:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0004_remove_applicationfield_application_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='data',
            field=models.JSONField(default=dict),
        ),
    ]
