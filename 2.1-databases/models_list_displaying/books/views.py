from django.core.paginator import Paginator
from django.shortcuts import render

from books.models import Book

def books_view(request):
    template = 'books/books_list.html'
    books_objects = Book.objects.all()

    context = {'books': books_objects}

    return render(request, template, context)

def book_scope(request, pub_date):
    template = 'books/book.html'
    books = Book.objects.filter(pub_date=pub_date)
    next_date = Book.objects.filter(pub_date__gt=pub_date).order_by('pub_date').first()
    prev_date = Book.objects.filter(pub_date__lt=pub_date).order_by('-pub_date').first()

    context = {'books': books}

    if next_date:
        context['next_page'] = next_date.pub_date

    if prev_date:
        context['prev_page'] = prev_date.pub_date

    return render(request, template, context)
