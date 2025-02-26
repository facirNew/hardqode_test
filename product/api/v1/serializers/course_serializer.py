from courses.models import Course, Group, Lesson
from django.contrib.auth import get_user_model
from django.db.models import Q, Count, Avg
from rest_framework import serializers
from users.models import CustomUser, Subscription

User = get_user_model()


class LessonSerializer(serializers.ModelSerializer):
    """Список уроков."""

    course = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Lesson
        fields = (
            'title',
            'link',
            'course',
        )


class CreateLessonSerializer(serializers.ModelSerializer):
    """Создание уроков."""

    class Meta:
        model = Lesson
        fields = (
            'title',
            'link',
            'course',
        )


class StudentSerializer(serializers.ModelSerializer):
    """Студенты курса."""

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
        )


class GroupSerializer(serializers.ModelSerializer):
    """Список групп."""

    class Meta:
        model = Group
        fields = ('group_number',)


class CreateGroupSerializer(serializers.ModelSerializer):
    """Создание групп."""

    class Meta:
        model = Group
        fields = (
            'group_number',
            'course',
        )


class MiniLessonSerializer(serializers.ModelSerializer):
    """Список названий уроков для списка курсов."""

    class Meta:
        model = Lesson
        fields = (
            'title',
        )


class CourseSerializer(serializers.ModelSerializer):
    """Список курсов."""

    lessons = MiniLessonSerializer(many=True, read_only=True)
    lessons_count = serializers.SerializerMethodField(read_only=True)
    students_count = serializers.SerializerMethodField(read_only=True)
    groups_filled_percent = serializers.SerializerMethodField(read_only=True)
    demand_course_percent = serializers.SerializerMethodField(read_only=True)

    def get_lessons_count(self, obj):
        """Количество уроков в курсе."""

        return Lesson.objects.filter(course=obj).count()

    def get_students_count(self, obj):
        """Общее количество студентов на курсе."""

        return Subscription.objects.filter(course=obj).count()

    def get_groups_filled_percent(self, obj):
        """Процент заполнения групп, если в группе максимум 30 чел.."""

        max_student = 30
        return (Group.objects.filter(course=self)
                .annotate(students_count=Count('student_group__student'))
                .aggregate(Avg('students_count'))) / max_student

    def get_demand_course_percent(self, obj):
        """Процент приобретения курса."""

        return round(Subscription.objects.filter(course=obj).count() / CustomUser.objects.all().count(), 2)

    class Meta:
        model = Course
        fields = (
            'id',
            'author',
            'title',
            'start_date',
            'price',
            'lessons_count',
            'lessons',
            'demand_course_percent',
            'students_count',
            'groups_filled_percent',
        )


class CreateCourseSerializer(serializers.ModelSerializer):
    """Создание курсов."""

    class Meta:
        model = Course
        fields = '__all__'


class AvailableCourseSerializator(serializers.ModelSerializer):
    """Доступные курсы"""

    available = serializers.SerializerMethodField(read_only=True)
    lessons = MiniLessonSerializer(many=True, read_only=True)
    lessons_count = serializers.SerializerMethodField(read_only=True)

    def get_available(self, obj):
        """Доступные курсы"""
        return obj.filter(Q(is_active=True) | ~Q(subscription_student=self.context['request'].user))

    def get_lessons_count(self, obj):
        """Количество уроков в курсе."""

        return Lesson.objects.filter(course=obj).count()

    class Meta:
        model = Course
        fields = (
            'id',
            'author',
            'title',
            'start_date',
            'price',
            'lessons_count',
        )
