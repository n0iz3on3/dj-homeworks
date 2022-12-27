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
    sorted_books_objects = Book.objects.all().order_by('pub_date')
    paginator = Paginator(sorted_books_objects, 1)
    context = {}

    for page, book in enumerate(sorted_books_objects, 1):
        if pub_date == book.pub_date:
            page_by_date = paginator.page(page)

            if page_by_date.has_previous():
                prev_page_by_date = paginator.page(page_by_date.previous_page_number()).object_list[0].pub_date
                context['prev_page'] = prev_page_by_date

            if page_by_date.has_next():
                next_page_by_date = paginator.page(page_by_date.next_page_number()).object_list[0].pub_date
                context['next_page'] = next_page_by_date

            context['book'] = book

    return render(request, template, context)
