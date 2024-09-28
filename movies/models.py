import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

# Для ситуаций, когда необходимо создать новый проект на Django
# с существующей базой данных, разработчики фреймворка создали
# команду python manage.py inspectdb.
# Она возвращает содержимое models.py, основанное на схеме БД,
# и позволяет пропустить этап описания моделей вручную.


class TimeStampedMixin(models.Model):
    # auto_now_add автоматически выставит дату создания записи
    created = models.DateTimeField(auto_now_add=True)
    # auto_now изменятся при каждом обновлении записи
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        # Этот параметр указывает Django, что этот класс не является представлением таблицы
        abstract = True


class UUIDMixin(models.Model):
    # Типичная модель в Django использует число в качестве id. В таких ситуациях поле не описывается в модели.
    # Вам же придётся явно объявить primary key.
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


# Указывать models.Model родителем Genre не обязательно,
# потому что этот класс уже является родителем у миксинов.
class Genre(UUIDMixin, TimeStampedMixin):
    # Первым аргументом обычно идёт человекочитаемое название поля
    name = models.CharField("Название", max_length=255)
    # blank=True делает поле необязательным для заполнения.
    description = models.TextField("Описание", blank=True)

    class Meta:
        # Ваши таблицы находятся в нестандартной схеме. Это нужно указать в классе модели
        db_table = 'content"."genre'  # Работает только с таким порядком кавычек
        # Следующие два поля отвечают за название модели в интерфейсе
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return self.name


class Person(UUIDMixin, TimeStampedMixin):
    class Gender(models.TextChoices):
        MALE = "male", _("male")
        FEMALE = "female", _("female")

    full_name = models.TextField("Полное имя")
    gender = models.TextField(_("gender"), choices=Gender.choices, null=True)

    class Meta:
        db_table = 'content"."person'
        verbose_name = "Персона"
        verbose_name_plural = "Персоны"

    def __str__(self):
        return self.full_name


class Filmwork(UUIDMixin, TimeStampedMixin):
    # class Filmtype(models.TextChoices):
    #     movie = ("movie", "movie")
    #     tv_show = ("tv_show", "tv_show")

    # Enumeration types
    class Filmtype(models.TextChoices):
        MOVIE = "movie", _("Фильм")
        TV_SHOW = "tv_show", _("Телепередача")

    certificate = models.CharField(_("certificate"), max_length=512, blank=True)
    file_path = models.FileField(_("file"), blank=True, null=True, upload_to="movies/")
    title = models.TextField("Название")
    description = models.TextField("Описание", blank=True)
    creation_date = models.DateField("Дата создания", blank=True)
    rating = models.FloatField(
        "Рейтинг", blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    type = models.CharField(
        "Тип",
        choices=Filmtype.choices,
        default=Filmtype.MOVIE,
    )
    genres = models.ManyToManyField(Genre, through="GenreFilmwork")
    persons = models.ManyToManyField(Person, through="PersonFilmwork")

    class Meta:
        db_table = 'content"."film_work'
        verbose_name = "Телефильм"
        verbose_name_plural = "Телефильмы"

    def __str__(self):
        return self.title


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey("Filmwork", on_delete=models.CASCADE)
    genre = models.ForeignKey("Genre", on_delete=models.CASCADE, verbose_name="Жанр")
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content"."genre_film_work'
        verbose_name = "Жанр телефильма"
        verbose_name_plural = "Жанры телефильма"


class PersonFilmwork(UUIDMixin):
    class RoleType(models.TextChoices):
        MALE = "actor", _("Actor")
        FEMALE = "creator", _("Creator")

    film_work = models.ForeignKey("Filmwork", on_delete=models.CASCADE)
    person = models.ForeignKey(
        "Person", on_delete=models.CASCADE, verbose_name="Персона"
    )
    created = models.DateTimeField(auto_now_add=True)
    profession = models.TextField(_("profession"), choices=RoleType.choices, null=True)
    role = models.TextField(_("role"), null=True)

    class Meta:
        db_table = 'content"."person_film_work'
        verbose_name = "Персона телефильма"
        verbose_name_plural = "Персоны телефильма"
