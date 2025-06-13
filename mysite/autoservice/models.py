from django.db import models

# Create your models here.
class CarModel(models.Model):
    make = models.CharField(verbose_name="Gamintojas", max_length=100)
    model = models.CharField(verbose_name="Modelis", max_length=100)

    def __str__(self):
        return f"{self.make} {self.model}"


class Service(models.Model):
    name = models.CharField(verbose_name="Pavadinimas", max_length=100)
    price = models.IntegerField(verbose_name="Kaina")

    def __str__(self):
        return self.name

class Car(models.Model):
    licence_plate = models.CharField(verbose_name="Valstybinis numeris", max_length=10)
    vin_number = models.CharField(verbose_name="VIN kodas", max_length=20)
    client_name = models.CharField(verbose_name="Klientas", max_length=20)
    car_model = models.ForeignKey(to="CarModel", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.car_model} ({self.licence_plate})"

