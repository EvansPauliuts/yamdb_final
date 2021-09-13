from datetime import date

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Avg

from users.models import User


class Categories(models.Model):
    name = models.CharField(max_length=50, verbose_name='Category')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='Slug')

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Genres(models.Model):
    name = models.CharField(max_length=50, verbose_name='Genre')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='Slug')

    class Meta:
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'

    def __str__(self):
        return self.name


def year_validator(value):
    if value > date.today().year:
        raise ValidationError(
            'Такой год еще не наступил',
            params={'value': value},
        )


class Titles(models.Model):
    name = models.CharField(max_length=50, verbose_name='Title')
    year = models.PositiveIntegerField(
        validators=[year_validator],
        db_index=True,
        verbose_name='Year'
    )
    category = models.ForeignKey(
        Categories,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='titles',
        verbose_name='Category'
    )
    genre = models.ManyToManyField(
        Genres,
        through='GenreTitle',
        related_name='titles',
        verbose_name='Genre'
    )
    description = models.TextField(verbose_name='Description')

    class Meta:
        verbose_name = 'Title'
        verbose_name_plural = 'Titles'

    @property
    def rating(self):
        score = self.reviews.filter(
            title=self
        ).aggregate(rating=Avg('score'))
        return score['rating']

    def __str__(self):
        return f'{self.name}'


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Titles, on_delete=models.CASCADE, verbose_name='Title'
    )
    genre = models.ForeignKey(
        Genres, on_delete=models.CASCADE, verbose_name='Genre'
    )

    class Meta:
        verbose_name = 'Title and genre'
        verbose_name_plural = 'Titles and genres'

    def __str__(self):
        return f'{self.title} {self.genre}'


class Review(models.Model):
    text = models.TextField(verbose_name='Text')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Author'
    )
    title = models.ForeignKey(
        Titles,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Title'
    )
    pub_date = models.DateTimeField(
        'Date public',
        auto_now_add=True
    )
    score = models.PositiveSmallIntegerField(
        'Score',
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ],
        default=1
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'

    def __str__(self):
        return f'{self.text}'


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Author'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Review'
    )
    text = models.TextField(verbose_name='Text')
    pub_date = models.DateTimeField(
        'Date public',
        auto_now_add=True
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return self.text
