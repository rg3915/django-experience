from django.urls import path

from backend.order import views as v

app_name = 'order'


urlpatterns = [
    path('', v.order_list, name='order_list'),
    path('create/', v.order_create, name='order_create'),
]
