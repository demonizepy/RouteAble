"""
URL configuration for map project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from main import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView # импорт классов для обработки аутентификации пользователей через API с использованием JSON Web Tokens из библиотеки Simple JWT

# routers для обработки запросов к API, создание маршрутов для получения списка всех объектов House, создания нового объекта House, получения данных конкретного объекта House по его первичному ключу, обновления данных этого объекта и удаления этого объекта

# router = routers.DefaultRouter()
# router.register(r'houses', views.HouseViewSet) # регистрация маршрута для обработки
# print(router.urls) # вывод зарегистрированных маршрутов для проверки правильности регистрации

urlpatterns = [
    # ------------------------------URL для обработки запросов на отображение страниц сайта---------------------------------
    path('admin/', admin.site.urls),
    path('', views.index),
    path('talk_People/', views.talk),
    path('Help_People/', views.help),
    path('Contact_People/', views.contact),
    
    # ------------------------------URL для обработки запросов к API---------------------------------
    path('api/v1/houses/', views.HouseAPIList.as_view()), # добавление URL для обработки GET и POST запросов, при обращении к этому URL будет вызван метод get() или post() класса HouseAPIList в зависимости от типа запроса
    path('api/v1/houses/<int:pk>/', views.HouseAPIUpdate.as_view()), # добавление URL для обработки GET и PUT запросов, при обращении к этому URL будет вызван метод get() или put() класса HouseAPIUpdate в зависимости от типа запроса
    path('api/v1/housesdelete/<int:pk>/', views.HouseAPIDestroy.as_view()), # добавление URL для обработки GET и DELETE запросов, при обращении к этому URL будет вызван метод get() или delete() класса HouseAPIDestroy в зависимости от типа запроса
    path('api/v1/map/', include('rest_framework.urls')), # добавление URL для обработки запросов на вход в систему, при обращении к этому URL будет вызван соответствующий метод класса LoginView из библиотеки Django REST Framework для обработки аутентификации пользователей через API
    
    # ------------------------------API для аутентификации пользователей через API с помощью библиотеки Djoser---------------------------------
    path('api/v1/auth/', include('djoser.urls')), # добавление URL для обработки запросов на регистрацию, вход в систему, выход из системы и изменение пароля, при обращении к этому URL будет вызван соответствующий метод класса UserViewSet из библиотеки Djoser для обработки аутентификации пользователей через API
    re_path('api/v1/auth/', include('djoser.urls.authtoken')), # добавление URL для обработки запросов на получение и удаление токена аутентификации, при обращении к этому URL будет вызван соответствующий метод класса TokenViewSet из библиотеки Djoser для обработки аутентификации пользователей через API с использованием токенов
    
    # ------------------------------API для аутентификации пользователей через API с помощью библиотеки Simple JWT---------------------------------
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # добавление URL для обработки запросов на получение пары токенов (access и refresh), при обращении к этому URL будет вызван метод post() класса TokenObtainPairView из библиотеки Simple JWT для обработки аутентификации пользователей через API с использованием JSON Web Tokens
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # добавление URL для обработки запросов на обновление access токена с помощью refresh токена, при обращении к этому URL будет вызван метод post() класса TokenRefreshView из библиотеки Simple JWT для обработки аутентификации пользователей через API с использованием JSON Web Tokens
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'), # добавление URL для обработки запросов на проверку действительности токена, при обращении к этому URL будет вызван метод post() класса TokenVerifyView из библиотеки Simple JWT для обработки аутентификации пользователей через API с использованием JSON Web Tokens
    
    # ------------------------------API для работы с объектами House---------------------------------
    # path('api/v1/', include(router.urls)), # добавление URL для обработки запросов к API, при обращении к этому URL будет вызван соответствующий метод класса HouseViewSet в зависимости от типа запроса и маршрута
    # path('api/v1/houses/', views.HouseViewSet.as_view({'get': 'list', 'post': 'create'})), # добавление URL для обработки GET и POST запросов, при обращении к этому URL будет вызван метод get() или post() класса HouseViewSet в зависимости от типа запроса
    # path('api/v1/houses/<int:pk>/', views.HouseViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})), # добавление URL для обработки GET, PUT и DELETE запросов, при обращении к этому URL будет вызван метод get(), put() или delete() класса HouseViewSet в зависимости от типа запроса, <int:pk> - это параметр URL, который передает первичный ключ объекта House для идентификации объекта, который нужно получить, обновить или удалить

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
