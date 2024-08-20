from django.db import models


class Course(models.Model):
    """Модель продукта - курса."""

    author = models.CharField(
        max_length=250,
        verbose_name='Автор',
    )
    title = models.CharField(
        max_length=250,
        verbose_name='Название',
    )
    start_date = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        verbose_name='Дата и время начала курса',
    )
    price = models.DecimalField(
        verbose_name='Стоимость',
        max_digits=10,
        decimal_places=2,
        default=0.00,
    )
    is_active = models.BooleanField(
        default=False,
        verbose_name='Курс доступен',
    )

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ('-id',)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    """Модель урока."""

    title = models.CharField(
        max_length=250,
        verbose_name='Название',
    )
    link = models.URLField(
        max_length=250,
        verbose_name='Ссылка',
    )
    course = models.ForeignKey(Course,
                               on_delete=models.CASCADE,
                               verbose_name='курс',
                               )

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ('id',)

    def __str__(self):
        return self.title


class Group(models.Model):
    """Модель группы."""

    group_number = models.PositiveSmallIntegerField(verbose_name='Номер группы')
    course = models.ForeignKey(Course, verbose_name='Курс', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        ordering = ('-id',)

    def __str__(self):
        return f'Группа курса {self.course} номер {self.group_number}'
