from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet

from students.filters import CourseFilter
from students.models import Course, StudentCourse
from students.serializers import CourseSerializer, StockSerializer


class CoursesViewSet(ModelViewSet):

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = (DjangoFilterBackend, )
    filterset_class = CourseFilter


class StudentCourseViewSet(ModelViewSet):

    queryset = StudentCourse.objects.all()
    serializer_class = StockSerializer
