from random import choice

import pytest
from model_bakery import baker
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
from rest_framework.test import APIClient

from students.models import Course, Student


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory


@pytest.fixture
def test_with_specific_settings(settings):
    settings.MAX_STUDENTS_PER_COURSE = 3
    assert settings.MAX_STUDENTS_PER_COURSE


@pytest.mark.django_db
def test_get_course_1(client, course_factory):
    # Arrange
    courses = course_factory(_quantity=1)
    # Act
    url = reverse('courses-detail', args='1')
    response = client.get(url)
    data = response.json()
    # Assert
    assert response.status_code == HTTP_200_OK
    assert data['id'] == courses[0].id


@pytest.mark.django_db
def test_get_courses(client, course_factory):
    courses = course_factory(_quantity=15)
    url = reverse('courses-list')
    response = client.get(url)
    data = response.json()
    assert response.status_code == HTTP_200_OK
    assert len(data) == len(courses)
    for index, course in enumerate(data):
        assert course['id'] == courses[index].id


@pytest.mark.django_db
def test_filter_courses_by_id(client, course_factory):
    courses = course_factory(_quantity=10)
    random_course = choice(courses)
    url = reverse('courses-list')
    filtered_course = {'id': str(random_course.id)}
    response = client.get(url, filtered_course)
    data = response.json()
    assert response.status_code == HTTP_200_OK
    assert len(data) == 1
    assert data[0]['id'] == random_course.id
    assert data[0]['name'] == random_course.name


@pytest.mark.django_db
def test_filter_courses_by_name(client, course_factory):
    courses = course_factory(_quantity=10)
    random_course = choice(courses)
    url = reverse('courses-list')
    filtered_course = {'name': str(random_course.name)}
    response = client.get(url, filtered_course)
    data = response.json()
    assert response.status_code == HTTP_200_OK
    assert len(data) == 1
    assert data[0]['id'] == random_course.id
    assert data[0]['name'] == random_course.name


@pytest.mark.django_db
def test_create_course(client):
    count = Course.objects.count()
    new_course = 'Kind, kind, python'
    url = reverse('courses-list')
    response = client.post(url, data={'name': new_course})
    data = response.json()
    assert response.status_code == HTTP_201_CREATED
    assert Course.objects.count() == count + 1
    assert data['name'] == new_course


@pytest.mark.django_db
def test_update_course_name(client, course_factory):
    course = course_factory(_quantity=1)
    course_id = course[0].id
    new_name = 'Python generation'
    url = reverse('courses-detail', args=[course_id])
    response = client.patch(url, data={'name': new_name})
    data = response.json()
    assert response.status_code == HTTP_200_OK
    assert data['id'] == course_id
    assert data['name'] == new_name


@pytest.mark.django_db
def test_remove_course(client, course_factory):
    course = course_factory(_quantity=1)
    course_id = course[0].id
    url = reverse('courses-detail', args=[course_id])
    response = client.delete(url)
    count = Course.objects.filter(id=course_id)
    assert response.status_code == HTTP_204_NO_CONTENT
    assert len(count) == 0


@pytest.mark.django_db
def test_add_student_to_course(client, course_factory, student_factory):
    course = course_factory(_quantity=1)
    student = student_factory(_quantity=1)
    url = reverse('stocks-list')
    course_student_response = client.post(url, data={'course': course[0].id, 'student': student[0].id})
    data = course_student_response.json()
    assert course_student_response.status_code == HTTP_201_CREATED
    assert data['student'] == student[0].id
    assert data['course'] == course[0].id


@pytest.mark.parametrize('students_count', [1, 2, 3, 5])
@pytest.mark.django_db
def test_course_student_limit(client, course_factory, student_factory, students_count, test_with_specific_settings):
    course = course_factory(_quantity=1)
    students = student_factory(_quantity=students_count)
    course_id = course[0].id
    url = reverse('stocks-list')
    for student in students:
        course_student_response = client.post(url, data={'course': course_id, 'student': student.id})
        if students.index(student) <= 3:
            assert course_student_response.status_code == HTTP_201_CREATED
        else:
            assert course_student_response.status_code == HTTP_400_BAD_REQUEST
