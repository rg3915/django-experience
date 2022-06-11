from django.urls import path

from backend.order import views as v

app_name = 'order'


urlpatterns = [
    path('order/', v.order_list, name='order_list'),
    path('order/create/', v.order_create, name='order_create'),
]
