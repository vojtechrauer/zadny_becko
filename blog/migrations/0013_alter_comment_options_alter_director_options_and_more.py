# Generated by Django 5.1.4 on 2025-02-17 15:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_alter_review_image_alter_review_rating'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'verbose_name': 'Komentář', 'verbose_name_plural': 'Komentáře'},
        ),
        migrations.AlterModelOptions(
            name='director',
            options={'verbose_name': 'Režisér', 'verbose_name_plural': 'Režiséři'},
        ),
        migrations.AlterModelOptions(
            name='film',
            options={'verbose_name': 'Film', 'verbose_name_plural': 'Filmy'},
        ),
        migrations.AlterModelOptions(
            name='review',
            options={'verbose_name': 'Recenze', 'verbose_name_plural': 'Recenze'},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'Uživatel', 'verbose_name_plural': 'Uživatelé'},
        ),
        migrations.CreateModel(
            name='FavoriteFilm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('film', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='in_favorites', to='blog.film')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite_films', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
