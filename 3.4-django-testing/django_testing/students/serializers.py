from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.conf import settings

from students.models import Course, StudentCourse


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ('id', 'name', 'students')


class StockSerializer(serializers.ModelSerializer):

    class Meta:
        model = StudentCourse
        fields = ('id', 'student', 'course')

    def validate(self, attrs):
        course = attrs['course']
        stock_limit = StudentCourse.objects.filter(course=course)
        if len(stock_limit) > settings.MAX_STUDENTS_PER_COURSE:
            raise ValidationError('maximum number of students per course')
        return attrs
