# Generated by Django 4.2.11 on 2024-10-04 14:18

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Filmwork',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='id')),
                ('title', models.TextField(verbose_name='title')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
                ('creation_date', models.DateField(blank=True, null=True, verbose_name='creation_date')),
                ('rating', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)], verbose_name='rating')),
                ('type', models.CharField(choices=[('movie', 'movie'), ('tv_show', 'tv_show')], verbose_name='type')),
            ],
            options={
                'verbose_name': 'film_work',
                'verbose_name_plural': 'film_works',
                'db_table': 'content"."film_work',
                'ordering': ['-modified'],
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='id')),
                ('name', models.CharField(max_length=255, verbose_name='name_title')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
            ],
            options={
                'verbose_name': 'genre',
                'verbose_name_plural': 'genres',
                'db_table': 'content"."genre',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='GenreFilmwork',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='id')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
            ],
            options={
                'verbose_name': 'genre_film_work',
                'verbose_name_plural': 'genres_film_work',
                'db_table': 'content"."genre_film_work',
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='id')),
                ('full_name', models.TextField(verbose_name='full_name')),
            ],
            options={
                'verbose_name': 'person',
                'verbose_name_plural': 'persons',
                'db_table': 'content"."person',
                'ordering': ['full_name'],
            },
        ),
        migrations.CreateModel(
            name='PersonFilmwork',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='id')),
                ('role', models.TextField(verbose_name='role')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('film_work', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.filmwork', verbose_name='film_work')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.person', verbose_name='person')),
            ],
            options={
                'verbose_name': 'person_film_work',
                'verbose_name_plural': 'persons_film_work',
                'db_table': 'content"."person_film_work',
            },
        ),
        migrations.AddIndex(
            model_name='person',
            index=models.Index(fields=['full_name'], name='person_full_name_idx'),
        ),
        migrations.AddField(
            model_name='genrefilmwork',
            name='film_work',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.filmwork', verbose_name='film_work'),
        ),
        migrations.AddField(
            model_name='genrefilmwork',
            name='genre',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.genre', verbose_name='genre'),
        ),
        migrations.AddIndex(
            model_name='genre',
            index=models.Index(fields=['name'], name='genre_name_idx'),
        ),
        migrations.AddField(
            model_name='filmwork',
            name='genres',
            field=models.ManyToManyField(through='movies.GenreFilmwork', to='movies.genre', verbose_name='genres'),
        ),
        migrations.AddField(
            model_name='filmwork',
            name='persons',
            field=models.ManyToManyField(through='movies.PersonFilmwork', to='movies.person', verbose_name='persons'),
        ),
        migrations.AddConstraint(
            model_name='personfilmwork',
            constraint=models.UniqueConstraint(fields=('film_work', 'person', 'role'), name='film_work_person_role_idx'),
        ),
        migrations.AddConstraint(
            model_name='genrefilmwork',
            constraint=models.UniqueConstraint(fields=('film_work', 'genre'), name='film_work_genre_idx'),
        ),
        migrations.AddIndex(
            model_name='filmwork',
            index=models.Index(fields=['title'], name='film_work_title_idx'),
        ),
        migrations.AddIndex(
            model_name='filmwork',
            index=models.Index(fields=['rating'], name='film_work_rating_idx'),
        ),
        migrations.AddIndex(
            model_name='filmwork',
            index=models.Index(fields=['type'], name='film_work_type_idx'),
        ),
    ]
