import pytest
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.test import APIClient
from django.urls import reverse
from model_bakery import baker
from random import choice

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
    params = {'name': new_course}
    url = reverse('courses-list')
    response = client.post(url, data=params)
    data = response.json()
    assert response.status_code == HTTP_201_CREATED
    assert Course.objects.count() == count + 1
    assert data['name'] == new_course


@pytest.mark.django_db
def test_update_course_name(client, course_factory):
    course = course_factory(_quantity=1)
    course_id = course[0].id
    new_name = 'Python generation'
    params = {'name': new_name}
    url = reverse('courses-detail', args=[course_id])
    response = client.patch(url, data=params)
    data = response.json()
    assert response.status_code == HTTP_200_OK
    assert data['id'] == course_id
    assert data['name'] == new_name


@pytest.mark.django_db
def test_update_course_student(client, course_factory, student_factory):
    course = course_factory(_quantity=1)
    student = student_factory(_quantity=1)
    # count_students_on_course = len(course['students'])
    course_id = course[0].id
    course_name = course[0].name
    student_id = student[0].id
    params = {'students': [student_id]}
    url = reverse('courses-detail', args=[course_id])
    response = client.patch(url, data=params)
    assert response.status_code == HTTP_200_OK
    # assert len(course['students']) == count_students_on_course + 1


# @pytest.mark.django_db
# def test_get_students(client, course_factory):
#     students = student_factory(_quantity=15)
#     response = client.get('/api/v1/courses/')
#     assert response.status_code == 200
#     data = response.json()
#     assert len(data) == len(students)
