from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime
from django.conf import settings
import markdown
from django.utils.safestring import mark_safe


class MyModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Country(MyModel):
    name = models.CharField("Название", max_length=200, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Страна"
        verbose_name_plural = "Страны"

    def __str__(self):
        return self.name


class Genre(MyModel):
    name = models.CharField("Название", max_length=200, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return self.name


class Person(MyModel):
    name = models.CharField("Имя", max_length=400)
    origin_name = models.CharField("Имя в оригинале", max_length=400,
                                   blank=True, null=True)
    birthday = models.DateField("Дата рождения", blank=True, null=True,
                                validators=[
                                    MaxValueValidator(
                                        limit_value=datetime.date.today)
                                ])
    photo = models.ImageField(
        "Фото", upload_to='photos/', blank=True, null=True)
    kinopoisk_id = models.PositiveIntegerField(
        "Kinopoisk ID", blank=True, null=True)

    def age(self):
        if not self.birthday:
            return None
        today = datetime.date.today()
        return today.year - self.birthday.year \
            - ((today.month, today.day) < (self.birthday.month,
                                           self.birthday.day))

    class Meta:
        ordering = ["name"]
        verbose_name = "Персона"
        verbose_name_plural = "Персоны"

    def __str__(self):
        return self.name


class Film(MyModel):
    name = models.CharField("Имя", max_length=1024)
    origin_name = models.CharField(
        "Название (в оригинале)", max_length=1024, blank=True, null=True)
    slogan = models.CharField("Девиз", max_length=2048, blank=True, null=True)
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, verbose_name="Страна")
    genres = models.ManyToManyField(Genre, verbose_name="Жанр")
    director = models.ForeignKey(
        Person, on_delete=models.CASCADE, verbose_name="Режиссер",
        related_name="directed_films")
    length = models.PositiveIntegerField(
        "Продолжительность", blank=True, null=True)
    year = models.PositiveIntegerField("Год выпуска", blank=True, null=True,
                                       validators=[MinValueValidator(
                                           limit_value=1885)])
    trailer_url = models.URLField("Трейлер", blank=True, null=True)
    cover = models.ImageField(
        "Постер", upload_to='covers/', blank=True, null=True)
    description = models.TextField("Описание", blank=True, null=True)
    people = models.ManyToManyField(Person, verbose_name="Актеры")
    kinopoisk_id = models.PositiveIntegerField(
        "Kinopoisk ID", blank=True, null=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"

    def __str__(self):
        return self.name

class Post(MyModel):
    name = models.CharField("Название", max_length=250)
    slug = models.SlugField(max_length=250)
    icon = models.ImageField(
        "Иконка", upload_to="post_images/", blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name="posts")

    class Meta:
        ordering = ["created_at"]
        verbose_name = "Новость"
        verbose_name_plural = "Новости"

    def __str__(self):
        return self.name
    
class Comment(MyModel):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name="comments")
    body = models.TextField("Текст", null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name="comments")
    
    class Meta:
        ordering = ["created_at"]
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return self.name

class Section(MyModel):
    class ImageStatus(models.TextChoices):
        LEFT = 'L', 'Left'
        RIGHT = 'R', 'Right'
        BEFORE_TITLE = 'BT', 'Before title'
        AFTER_TITLE = "AT", 'After title'
        BOTTOM = 'B', 'Bottom'

    name = models.CharField("Название", max_length=250)
    body = models.TextField("Текст", null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name="sections")
    position = models.IntegerField("Позиция")
    image = models.ImageField(
        "Изображение", upload_to="post_images/", blank=True, null=True)
    image_status = models.CharField(max_length=2, choices=ImageStatus.choices,
                                    default=ImageStatus.BEFORE_TITLE)

    class Meta:
        ordering = ["position"]
        verbose_name = "Секция"
        verbose_name_plural = "Секции"

    def __str__(self):
        return self.name
    
    def body_as_markdown(self):
        return mark_safe(markdown.markdown(self.body))  