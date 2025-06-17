from django.db import models


# Create your models here.
class CarModel(models.Model):
    make = models.CharField(verbose_name="Gamintojas", max_length=100)
    model = models.CharField(verbose_name="Modelis", max_length=100)

    class Meta:
        verbose_name = "Automobilio modelis"
        verbose_name_plural = "Automobilio modeliai"

    def __str__(self):
        return f"{self.make} {self.model}"


class Service(models.Model):
    name = models.CharField(verbose_name="Pavadinimas", max_length=100)
    price = models.IntegerField(verbose_name="Kaina")

    class Meta:
        verbose_name = "Paslauga"
        verbose_name_plural = "Paslaugos"

    def __str__(self):
        return self.name


class Car(models.Model):
    licence_plate = models.CharField(verbose_name="Valstybinis numeris", max_length=10)
    vin_number = models.CharField(verbose_name="VIN kodas", max_length=20)
    client_name = models.CharField(verbose_name="Klientas", max_length=20)
    car_model = models.ForeignKey(to="CarModel", on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "Automobilis"
        verbose_name_plural = "Automobiliai"


    def __str__(self):
        return f"{self.car_model} ({self.licence_plate})"


class Order(models.Model):
    car = models.ForeignKey(to="Car", verbose_name="Automobilis", on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateTimeField(verbose_name="Data", auto_now_add=True)

    # TODO total

    class Meta:
        verbose_name = "Užsakymas"
        verbose_name_plural = "Užsakymai"

    def __str__(self):
        return f"{self.car} - {self.date}, total: {self.total()}"

    def total(self):
        lines = self.lines.all()
        result = 0
        for line in lines:
            result += line.service.price * line.qty
        return result


class OrderLine(models.Model):
    order = models.ForeignKey(to="Order", verbose_name="Užsakymas", on_delete=models.CASCADE, related_name="lines")
    service = models.ForeignKey(to="Service", verbose_name="Paslauga", on_delete=models.SET_NULL, null=True, blank=True)
    qty = models.IntegerField(verbose_name="Kiekis")

    # TODO sum

    def line_sum(self):
        return self.service.price * self.qty

    class Meta:
        verbose_name = "Užsakymo eilutė"
        verbose_name_plural = "Užsakymo eilutės"

    def __str__(self):
        return f"{self.service} ({self.service.price}) * {self.qty} = {self.line_sum()} ({self.order.date})"
