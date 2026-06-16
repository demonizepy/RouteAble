from django.shortcuts import render, redirect
from main.models import House, Elevator
from rest_framework import generics, viewsets
from .serializers import HouseSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.forms.models import model_to_dict
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .permissions import IsAdminReadOnly, IsOwnerOrReadOnly
from rest_framework.authentication import TokenAuthentication
from .pagination import HouseApiListPagination
from .forms import HouseForm
from django.contrib.auth.decorators import login_required
# Create perfomance 

# ------------------------------Представления для обработки запросов на отображение страниц сайта---------------------------------
def index(request):
    h = House.objects.all()
    return render(request, 'index.html', {'houses': h})

# Create your views here.
def talk(request):
    return render(request, 'page1.html')

def help(request):
    return render(request, 'page2.html')

def contact(request):
    return render(request, 'page3.html')

def map_view(request):
    form = HouseForm()
    return render(request, 'map.html', {'form': form})


@login_required(login_url='/login/')
def map_view(request):
    if request.method == 'POST':
        house_id = request.POST.get('house_id')
        
        # Если редактируем существующий дом — берем его, иначе создаем новый
        instance = House.objects.filter(id=house_id).first() if house_id else None
        form = HouseForm(request.POST, instance=instance)
        
        if form.is_valid():
            house = form.save(commit=False)
            house.latitude = request.POST.get('latitude')
            house.longitude = request.POST.get('longitude')
            
            if request.user.is_authenticated:
                house.user = request.user
            
            # 1. Сначала сохраняем дом, чтобы зафиксировать связь с лифтом
            house.save()

            # 2. Получаем размеры из очищенных данных формы
            width = form.cleaned_data.get('elevator_width')
            length = form.cleaned_data.get('elevator_length')

            # 3. Сохраняем размеры непосредственно в привязанный объект лифта
            if house.elevator and "Есть" in house.elevator.condition:
                # Если ширина и длина были введены пользователем
                if width is not None and length is not None:
                    house.elevator.size_width = width
                    house.elevator.size_length = length
                    house.elevator.save() # Сохраняем изменения в таблицу Elevator

            return redirect('/map/')
    else:
        form = HouseForm()

    houses = House.objects.all()
    return render(request, 'map.html', {'form': form, 'houses': houses})

# -----------------------------API для работы с объектами House---------------------------------

# -----------3 базовых класса для объяснения работы ограничения доступа к данным через API------

class HouseAPIList(generics.ListCreateAPIView): # API get запрос для получения списка всех объектов House и POST запрос для создания нового объекта House, данные передаются в формате JSON
    queryset = House.objects.all()
    serializer_class = HouseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly] # разрешение доступа к этому API для всех пользователей, включая неавторизованных, без ограничения доступа к данным, данные передаются в формате JSON
    pagination_class = HouseApiListPagination # добавление пагинации для этого API, что позволяет клиенту получать данные порциями и управлять количеством данных, получаемых за один запрос, данные передаются в формате JSON

class HouseAPIUpdate(generics.RetrieveUpdateAPIView): # API get запрос для получения данных конкретного объекта House по его первичному ключу 
    # и PUT запрос для обновления данных этого объекта, данные передаются в формате JSON
    queryset = House.objects.all()
    serializer_class = HouseSerializer
    permission_classes = [IsAuthenticated] # разрешение доступа к этому API для всех пользователей, включая неавторизованных, без ограничения доступа к данным, данные передаются в формате JSON
    # authentication_classes = [TokenAuthentication] # добавление аутентификации с помощью токенов для этого API, что позволяет ограничить доступ к данным только для авторизованных пользователей, данные передаются в формате JSON
    
class HouseAPIDestroy(generics.RetrieveDestroyAPIView): # API get запрос для получения данных конкретного объекта House по его первичному ключу, 
    # и DELETE запрос для удаления этого объекта, данные передаются в формате JSON
    queryset = House.objects.all()
    serializer_class = HouseSerializer
    permission_classes = [IsAdminReadOnly] # разрешение доступа к этому API для всех пользователей, включая неавторизованных, без ограничения доступа к данным, данные передаются в формате JSON

# class HouseViewSet(viewsets.ModelViewSet): # API для получения списка всех объектов House, создания нового объекта House, получения данных конкретного объекта House по его первичному ключу, обновления данных этого объекта и удаления этого объекта, данные передаются в формате JSON
#     queryset = House.objects.all()
#     serializer_class = HouseSerializer

#     def get_queryset(self): # переопределение метода get_queryset() для получения всех объектов House из базы данных, преобразования их в список словарей с помощью model_to_dict() и возвращения этого списка, данные передаются в формате JSON
#         pk = self.kwargs.get('pk', None) # получение первичного ключа объекта House из URL для идентификации объекта, который нужно получить, обновить или удалить
#         if not pk:
#             return House.objects.all()[:4] # ограничение количества объектов House, возвращаемых при GET запросе, до 4 для оптимизации производительности и уменьшения нагрузки на сервер при обработке большого количества данных
        
#         return House.objects.filter(pk=pk) # возвращение объекта House, который соответствует первичному ключу, переданному в URL, данные передаются в формате JSON
        
#     @action(detail=False, methods=['get']) # добавление дополнительного маршрута для получения всех объектов House в виде списка словарей, при обращении к этому маршруту будет вызван метод get_all_houses(), который возвращает список всех объектов House в виде словарей, данные передаются в формате JSON
#     def getall(self, request):
#         houses = House.objects.all()
#         serializer = HouseSerializer(houses, many=True)
#         return Response(serializer.data)

# class HouseAPIList(generics.ListCreateAPIView): # API get запрос для получения списка всех объектов House и POST запрос для создания нового объекта House, данные передаются в формате JSON
#     queryset = House.objects.all()
#     serializer_class = HouseSerializer

# class HouseAPIUpdate(generics.RetrieveUpdateAPIView): # API get запрос для получения данных конкретного объекта House по его первичному ключу 
#     # и PUT запрос для обновления данных этого объекта, данные передаются в формате JSON
#     queryset = House.objects.all()
#     serializer_class = HouseSerializer

# class HouseAPIDetailView(generics.RetrieveUpdateDestroyAPIView): # API get запрос для получения данных конкретного объекта House по его первичному ключу, 
#     # PUT запрос для обновления данных этого объекта и DELETE запрос для удаления этого объекта, данные передаются в формате JSON
#     queryset = House.objects.all()
#     serializer_class = HouseSerializer



# ---------начальное API для работы с объектами House с помощью класса APIView------------------
# class HouseAPIView(APIView): # API get запрос без сериализатора, выводит фиксированное сообщение
#     def get(self, request):
#         spk = House.objects.all()
#         return Response({'title': HouseSerializer(spk, many=True).data, 'message': 'This is GET request'})
    
#     def post(self, request): # Добавление в базу данных нового объекта House через POST запрос, данные передаются в формате JSON
#         serializer = HouseSerializer(data=request.data) # создание экземпляра сериализатора HouseSerializer с данными из POST запроса
#         serializer.is_valid(raise_exception=True) # проверка данных на валидность, если данные не валидны, будет выброшено исключение с сообщением об ошибке
#         serializer.save() # сохранение нового объекта House в базе данных на основе проверенных данных, метод save() вызывает метод create() сериализатора, 
#                         # который создает новый объект House с помощью модели и сохраняет его в базе данных        
        
#         return Response({'title': serializer.data, 'message': 'This is POST request'}) # возвращение ответа с данными нового объекта House в формате JSON 
#                                                                                         #и сообщением о том, что это POST запрос

#     def put(self, request, *args, **kwargs): # Обновление и изменение существующего объекта House через PUT запрос, данные передаются в формате JSON
#         pk = kwargs.get('pk', None) # получение первичного ключа объекта House из URL для идентификации объекта, который нужно обновить
#         if not pk:
#             return Response({'error': 'Primary key is required'}, status=400)
#         try:
#             house = House.objects.get(pk=pk)
#         except House.DoesNotExist:
#             return Response({'error': 'House not found'}, status=404)
#         serializer = HouseSerializer(data=request.data, instance=house) # создание экземпляра сериализатора HouseSerializer с данными из PUT запроса и существующим объектом House, который нужно обновить
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({'title': serializer.data, 'message': 'This is PUT request'}) # возвращение ответа с данными обновленного объекта House в формате JSON
#                                                                                         #и сообщением о том, что это PUT запрос
    
#     def delete(self, request, *args, **kwargs): # Удаление существующего объекта House через DELETE запрос
#         pk = kwargs.get('pk', None) # получение первичного ключа объекта House из URL для идентификации объекта, который нужно удалить
#         if not pk:
#             return Response({'error': 'Primary key is required'}, status=400)
#         try:
#             house = House.objects.get(pk=pk)
#         except House.DoesNotExist:
#             return Response({'error': 'House not found'}, status=404)
#         house.delete() # удаление объекта House из базы данных
#         return Response({'message': 'House deleted successfully'}) # возвращение ответа с сообщением об успешном удалении объекта House

# class HouseAPIView(generics.ListAPIView):
#     queryset = House.objects.all()
#     serializer_class = HouseSerializer