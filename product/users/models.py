from courses.models import Course, Group
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class CustomUser(AbstractUser):
    """Кастомная модель пользователя - студента."""

    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=250,
        unique=True,
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = (
        'username',
        'first_name',
        'last_name',
        'password',
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('-id',)

    def __str__(self):
        return self.get_full_name()


class Balance(models.Model):
    """Модель баланса пользователя."""

    user = models.ForeignKey(CustomUser,
                             on_delete=models.CASCADE,
                             related_name='balance',
                             verbose_name='Пользователь',
                             )
    amount = models.DecimalField(max_digits=10,
                                 decimal_places=2,
                                 default=1000.00,
                                 )

    class Meta:
        verbose_name = 'Баланс'
        verbose_name_plural = 'Балансы'
        ordering = ('-id',)

    def __str__(self):
        return f'{self.user.username} - {self.amount} бонусов'

    def save(self, *args, **kwargs):
        if self.amount < 0:
            raise ValidationError('Баланс не может быть отрицательным.')
        super().save(*args, **kwargs)


class Subscription(models.Model):
    """Модель подписки пользователя на курс."""

    student = models.ForeignKey(
        CustomUser,
        related_name='subscription',
        on_delete=models.CASCADE,
        verbose_name='Студент',
    )
    course = models.ForeignKey(
        Course,
        related_name='subscription',
        on_delete=models.CASCADE,
        verbose_name='Курс',
    )
    enrolled_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата подписки',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        unique_together = (('student', 'course'), )
        ordering = ('-id',)

    def __str__(self):
        return f'{self.course} {self.student}'


class GroupEnrollment(models.Model):
    """Принадлежность студента группе"""

    group = models.ForeignKey(Group,
                              verbose_name='Группа',
                              on_delete=models.CASCADE,
                              related_name='student_group',
                              )
    student = models.ForeignKey(CustomUser,
                                verbose_name='Студент',
                                on_delete=models.CASCADE,
                                related_name='student_group',
                                )

    class Meta:
        verbose_name = 'Запись в группу'
        verbose_name_plural = 'Записи в группы'
        ordering = ('-id',)

    def __str__(self):
        return f'Студент {self.student} в {self.group}'
