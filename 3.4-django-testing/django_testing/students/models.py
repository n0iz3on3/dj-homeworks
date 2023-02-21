from django.db import models


class Student(models.Model):

    name = models.TextField()

    birth_date = models.DateField(
        null=True,
    )


class Course(models.Model):

    name = models.TextField()

    students = models.ManyToManyField(
        Student,
        blank=True,
        through='StudentCourse'
    )


class StudentCourse(models.Model):

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='stocks'
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='stocks'
    )
