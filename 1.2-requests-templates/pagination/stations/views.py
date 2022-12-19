from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse
from pagination.settings import BUS_STATION_CSV
import csv

def index(request):
    return redirect(reverse('bus_stations'))


with open(BUS_STATION_CSV, newline='', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        data = [row for row in reader]

def bus_stations(request):
    page_number = int(request.GET.get('page', 1))
    paginator = Paginator(data, 10)
    page = paginator.get_page(page_number)
    bus_stations_list = page.object_list
    context = {
         'bus_stations': bus_stations_list,
         'page': page,
    }
    return render(request, 'stations/index.html', context)
