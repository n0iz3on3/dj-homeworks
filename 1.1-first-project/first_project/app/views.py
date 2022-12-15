from django.http import HttpResponse
from django.shortcuts import render, reverse
from time import localtime, asctime
import os


def home_view(request):
    template_name = 'app/home.html'
    pages = {
        'Главная страница': reverse('home'),
        'Показать текущее время': reverse('time'),
        'Показать содержимое рабочей директории': reverse('workdir')
    }

    context = {
        'pages': pages
    }
    return render(request, template_name, context)


def time_view(request):
    sec_time = localtime()
    current_time = asctime(sec_time)
    msg = f'Текущая дата и время: {current_time}'
    return HttpResponse(msg)


def workdir_view(request):
    path = '.'
    result = sorted(os.listdir(path))
    template_name = 'app/files.html'
    files_list = [f'{index + 1} - {file}'
                  for index, file in enumerate(result)]

    return render(request, template_name, context={'files_list': files_list})
