# Generated by Django 5.1.4 on 2025-03-21 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0020_alter_film_image_alter_review_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='director',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='directors/'),
        ),
    ]
