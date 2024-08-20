from api.v1.permissions import IsStudentOrIsAdmin, ReadOnlyOrIsAdmin
from api.v1.serializers.course_serializer import (
    AvailableCourseSerializator,
    CourseSerializer,
    CreateCourseSerializer,
    CreateGroupSerializer,
    CreateLessonSerializer,
    GroupSerializer,
    LessonSerializer,
)

# from api.v1.serializers.user_serializer import SubscriptionSerializer
from courses.models import Course
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from users.models import Subscription


class LessonViewSet(viewsets.ModelViewSet):
    """Уроки."""

    permission_classes = (IsStudentOrIsAdmin,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return LessonSerializer
        return CreateLessonSerializer

    def perform_create(self, serializer):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        serializer.save(course=course)

    def get_queryset(self):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        return course.lessons.all()


class GroupViewSet(viewsets.ModelViewSet):
    """Группы."""

    permission_classes = (permissions.IsAdminUser,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return GroupSerializer
        return CreateGroupSerializer

    def perform_create(self, serializer):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        serializer.save(course=course)

    def get_queryset(self):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        return course.groups.all()


class CourseViewSet(viewsets.ModelViewSet):
    """Курсы """

    queryset = Course.objects.all()
    permission_classes = (ReadOnlyOrIsAdmin,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return CourseSerializer
        return CreateCourseSerializer

    @action(
        methods=['post'],
        detail=True,
        permission_classes=(permissions.IsAuthenticated,),
    )
    def pay(self, request, pk):
        """Покупка доступа к курсу (подписка на курс)."""

        user = self.request.user
        course = Course.objects.get_object_or_404(pk=pk)
        if Course.objects.filter(subscription_student=user):
            return Response(
                data={'error': 'Вы уже записаны на этот курс'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if user.balance.amount < course.price:
            return Response(
                data={'error': 'Недостаточно баллов'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            with transaction.atomic():
                user.balance = user.balance - course.price
                Subscription.object.create(student=user, course=course)
                user.save()
        except:
            return Response(
                data={'error': 'Ошибка записи на курс'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        data = {'success': 'Вы успешно записаны на курс'}
        return Response(
            data=data,
            status=status.HTTP_201_CREATED,
        )


class AvailableCourseViewSet(viewsets.ModelViewSet):
    """Доступные курсы"""

    serializer_class = AvailableCourseSerializator
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Course.objects.filter(Q(is_active=True) | ~Q(subscription_student=self.request.user))
