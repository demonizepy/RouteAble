from urllib.parse import quote

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.http import HttpResponseForbidden
from django.urls import reverse
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser

from main.models import House, Availability
from .forms import HouseForm, RegisterForm
from .serializers import HouseSerializer
from .permissions import IsAdminReadOnly
from .pagination import HouseApiListPagination


# ------------------------------ Отображение страниц ---------------------------------

def index(request):
    houses = House.objects.all()
    return render(request, 'index.html', {'houses': houses})

def talk(request):
    return render(request, 'page1.html')

def help(request):
    return render(request, 'page2.html')

def contact(request):
    return render(request, 'page3.html')

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация успешна.')
            return redirect('map')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


def map_view(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            next_url = quote(request.get_full_path())
            return redirect(f"/accounts/login/?next={next_url}")

        house_id = request.POST.get('house_id')
        instance = House.objects.filter(id=house_id).first() if house_id else None

        if instance and not request.user.is_staff:
            return HttpResponseForbidden('Изменение домов доступно только администраторам.')

        form = HouseForm(request.POST, instance=instance)

        if form.is_valid():
            house = form.save(commit=False)

            lat = request.POST.get('latitude')
            lng = request.POST.get('longitude')
            if lat:
                house.latitude = float(lat)
            if lng:
                house.longitude = float(lng)

            if instance is None:
                house.user = request.user
            else:
                house.user = instance.user

            house.save()
            return redirect('map')
    else:
        form = HouseForm()

    return render(request, 'map.html', {'form': form})


# ----------------------------- API Классы DRF ---------------------------------

class HouseAPIList(generics.ListCreateAPIView):
    queryset = House.objects.select_related('availability').all()
    serializer_class = HouseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = HouseApiListPagination

class HouseAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = House.objects.all()
    serializer_class = HouseSerializer
    permission_classes = [IsAdminUser]
    
class HouseAPIDestroy(generics.RetrieveDestroyAPIView):
    queryset = House.objects.all()
    serializer_class = HouseSerializer
    permission_classes = [IsAdminReadOnly]