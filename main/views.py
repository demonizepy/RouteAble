from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from main.models import House, Availability
from .forms import HouseForm
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


@login_required(login_url='/login/')
def map_view(request):
    if request.method == 'POST':
        house_id = request.POST.get('house_id')
        instance = House.objects.filter(id=house_id).first() if house_id else None
        
        form = HouseForm(request.POST, instance=instance)
        
        if form.is_valid():
            house = form.save(commit=False)
            
            lat = request.POST.get('latitude')
            lng = request.POST.get('longitude')
            if lat: 
                house.latitude = float(lat)
            if lng: 
                house.longitude = float(lng)
            
            house.user = request.user
            house.save()
            
            return redirect('/map/')
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
    permission_classes = [IsAuthenticated]
    
class HouseAPIDestroy(generics.RetrieveDestroyAPIView):
    queryset = House.objects.all()
    serializer_class = HouseSerializer
    permission_classes = [IsAdminReadOnly]