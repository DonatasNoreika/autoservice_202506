from django.urls import path
from .views import (index,
                    cars,
                    car,
                    search,
                    register,
                    profile,
                    OrderListView,
                    OrderDetailView,
                    UserOrderListView,
                    UserOrderCreateView)

urlpatterns = [
    path("", index, name="index"),
    path("cars/", cars, name="cars"),
    path("cars/<int:car_id>", car, name="car"),
    path("orders/", OrderListView.as_view(), name="orders"),
    path('search/', search, name='search'),
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    path("userorders/", UserOrderListView.as_view(), name="userorders"),
    path("orders/<int:pk>", OrderDetailView.as_view(), name="order"),
    path("orders/create", UserOrderCreateView.as_view(), name="orders_create"),
]
