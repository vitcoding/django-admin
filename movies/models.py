import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(_("created"), auto_now_add=True)
    modified = models.DateTimeField(_("modified"), auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(
        _("id"), primary_key=True, default=uuid.uuid4, editable=False
    )

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_("name_title"), max_length=255)
    description = models.TextField(_("description"), blank=True)

    class Meta:
        db_table = 'content"."genre'
        verbose_name = _("genre")
        verbose_name_plural = _("genres")
        ordering = ["name"]

        indexes = [
            models.Index(
                fields=["name"],
                name="genre_name_idx",
            ),
        ]

    def __str__(self):
        return self.name


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.TextField(_("full_name"))

    class Meta:
        db_table = 'content"."person'
        verbose_name = _("person")
        verbose_name_plural = _("persons")
        ordering = ["full_name"]

        indexes = [
            models.Index(
                fields=["full_name"],
                name="person_full_name_idx",
            ),
        ]

    def __str__(self):
        return self.full_name


class Filmwork(UUIDMixin, TimeStampedMixin):
    class Filmtype(models.TextChoices):
        MOVIE = "movie", _("movie")
        TV_SHOW = "tv_show", _("tv_show")

    title = models.TextField(_("title"))
    description = models.TextField(_("description"), blank=True)
    creation_date = models.DateField(_("creation_date"), blank=True)
    rating = models.FloatField(
        _("rating"),
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    type = models.CharField(
        _("type"),
        choices=Filmtype.choices,
    )
    genres = models.ManyToManyField(
        Genre, through="GenreFilmwork", verbose_name=_("genres")
    )
    persons = models.ManyToManyField(
        Person, through="PersonFilmwork", verbose_name=_("persons")
    )

    class Meta:
        db_table = 'content"."film_work'
        verbose_name = _("film_work")
        verbose_name_plural = _("film_works")
        ordering = ["-modified"]

        indexes = [
            models.Index(
                fields=["title"],
                name="film_work_title_idx",
            ),
            models.Index(
                fields=["rating"],
                name="film_work_rating_idx",
            ),
            models.Index(
                fields=["type"],
                name="film_work_type_idx",
            ),
        ]

    def __str__(self):
        return self.title


class GenreFilmwork(UUIDMixin):
    genre = models.ForeignKey(
        "Genre", on_delete=models.CASCADE, verbose_name=_("genre")
    )
    film_work = models.ForeignKey(
        "Filmwork", on_delete=models.CASCADE, verbose_name=_("film_work")
    )
    created = models.DateTimeField(_("created"), auto_now_add=True)

    class Meta:
        db_table = 'content"."genre_film_work'
        verbose_name = _("genre_film_work")
        verbose_name_plural = _("genres_film_work")

        indexes = [
            models.Index(
                fields=["film_work", "genre"],
                name="film_work_genre_idx",
            ),
        ]
        unique_together = [
            ["film_work", "genre"],
        ]


class PersonFilmwork(UUIDMixin):
    person = models.ForeignKey(
        "Person", on_delete=models.CASCADE, verbose_name=_("person")
    )
    film_work = models.ForeignKey(
        "Filmwork", on_delete=models.CASCADE, verbose_name=_("film_work")
    )
    role = models.TextField(_("role"))
    created = models.DateTimeField(_("created"), auto_now_add=True)

    class Meta:
        db_table = 'content"."person_film_work'
        verbose_name = _("person_film_work")
        verbose_name_plural = _("persons_film_work")

        indexes = [
            models.Index(
                fields=["film_work", "person"],
                name="film_work_person_idx",
            ),
        ]
        unique_together = [
            ["film_work", "person"],
        ]
