# Generated by Django 5.1.4 on 2025-01-25 13:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='film',
        ),
    ]
