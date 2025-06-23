from django.shortcuts import render
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Service, Order, Car


# Create your views here.
def index(request):
    context = {
        "num_services": Service.objects.count(),
        "num_orders_done": Order.objects.filter(status__exact='i').count(),
        "num_cars": Car.objects.count(),
    }
    return render(request, template_name="index.html", context=context)


def cars(request):
    paginator = Paginator(Car.objects.all(), per_page=5)
    page_number = request.GET.get('page')
    paged_cars = paginator.get_page(page_number)
    return render(request, template_name="cars.html", context={"cars": paged_cars})


def car(request, car_id):
    return render(request, template_name="car.html", context={"car": Car.objects.get(pk=car_id)})


class OrderListView(generic.ListView):
    model = Order
    template_name = "orders.html"
    context_object_name = "orders"
    paginate_by = 3


class OrderDetailView(generic.DetailView):
    model = Order
    template_name = "order.html"
    context_object_name = "order"


def search(request):
    """
    paprasta paieška. query ima informaciją iš paieškos laukelio,
    search_results prafiltruoja pagal įvestą tekstą knygų pavadinimus ir aprašymus.
    Icontains nuo contains skiriasi tuo, kad icontains ignoruoja ar raidės
    didžiosios/mažosios.
    """
    query = request.GET.get('query')

    car_search_results = Car.objects.filter(
        Q(client_name__icontains=query) | Q(car_model__make__icontains=query) | Q(
            car_model__model__icontains=query) | Q(
            licence_plate__icontains=query) | Q(vin_number__icontains=query))

    context = {
        "query": query,
        "cars": car_search_results,
    }
    return render(request, template_name="search.html", context=context)
