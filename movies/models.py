import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


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


class Filmwork(UUIDMixin, TimeStampedMixin):
    # class Filmtype(models.TextChoices):
    #     movie = ("movie", "movie")
    #     tv_show = ("tv_show", "tv_show")

    # Enumeration types
    class Filmtype(models.TextChoices):
        MOVIE = "movie", _("Фильм")
        TV_SHOW = "tv_show", _("Телепередача")

    title = models.TextField("Название")
    description = models.TextField("Описание", blank=True)
    creation_date = models.DateField("Дата создания", blank=True)
    rating = models.FloatField("Рейтинг", blank=True)
    type = models.CharField(
        "Тип",
        choices=Filmtype.choices,
        default=Filmtype.MOVIE,
    )

    class Meta:
        db_table = 'content"."film_work'
        verbose_name = "Телефильм"
        verbose_name_plural = "Телефильмы"

    def __str__(self):
        return self.title
