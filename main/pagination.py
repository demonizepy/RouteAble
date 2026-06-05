from rest_framework.pagination import PageNumberPagination

# ------------------------------Класс для настройки пагинации при обработке запросов на получение списка объектов House через API---------------------------------
class HouseApiListPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'size'
    max_page_size = 100
    
    