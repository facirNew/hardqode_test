from django.db.models import Count
from django.db.models.signals import post_save
from django.dispatch import receiver
from product import settings
from users.models import Balance, GroupEnrollment, Subscription

from courses.models import Course, Group


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_balance(sender, instance, created, **kwargs):
    """
    Создание баланса для пользователя
    """

    if created:
        Balance.objects.create(user=instance)


@receiver(post_save, sender=Course)
def create_course_groups(sender, instance, created, **kwargs):
    """
    Создание десяти групп для курса
    """

    if created:
        Group.objects.bulk_create(
            [Group(group_number=i, course=instance) for i in range(1, 11)],
        )


@receiver(post_save, sender=Subscription)
def post_save_subscription(sender, instance: Subscription, created, **kwargs):
    """
    Распределение нового студента в группу курса.
    """

    if created:
        group = Group.objects.filter(course=instance.course). \
            annotate(students_count=Count('student_group__student')). \
            order_by('students_count')[0]
        GroupEnrollment.objects.create(group=group, student=instance.student)
