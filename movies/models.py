import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# python manage.py makemessages -l en -l ru
# python manage.py compilemessages -l en -l ru
from django.utils.translation import gettext_lazy as _

# Для ситуаций, когда необходимо создать новый проект на Django
# с существующей базой данных, разработчики фреймворка создали
# команду python manage.py inspectdb.
# Она возвращает содержимое models.py, основанное на схеме БД,
# и позволяет пропустить этап описания моделей вручную.


class TimeStampedMixin(models.Model):
    # auto_now_add автоматически выставит дату создания записи
    created = models.DateTimeField(_("created"), auto_now_add=True)
    # auto_now изменятся при каждом обновлении записи
    modified = models.DateTimeField(_("modified"), auto_now=True)

    class Meta:
        # Этот параметр указывает Django,
        # что этот класс не является представлением таблицы
        abstract = True


class UUIDMixin(models.Model):
    # Типичная модель в Django использует число в качестве id.
    # В таких ситуациях поле не описывается в модели.
    # Вам же придётся явно объявить primary key.
    id = models.UUIDField(
        _("id"), primary_key=True, default=uuid.uuid4, editable=False
    )

    class Meta:
        abstract = True


# Указывать models.Model родителем Genre не обязательно,
# потому что этот класс уже является родителем у миксинов.
class Genre(UUIDMixin, TimeStampedMixin):
    # Первым аргументом обычно идёт человекочитаемое название поля
    name = models.CharField(_("name_title"), max_length=255)
    # blank=True делает поле необязательным для заполнения.
    description = models.TextField(_("description"), blank=True)

    class Meta:
        # Ваши таблицы находятся в нестандартной схеме.
        # Это нужно указать в классе модели

        # Работает только с таким порядком кавычек
        db_table = 'content"."genre'
        # Следующие два поля отвечают за название модели в интерфейсе
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
    # class Filmtype(models.TextChoices):
    #     movie = ("movie", "movie")
    #     tv_show = ("tv_show", "tv_show")

    # Enumeration types
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
        # default=Filmtype.MOVIE,
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
