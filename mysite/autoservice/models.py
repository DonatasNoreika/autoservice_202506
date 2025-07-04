from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from tinymce.models import HTMLField
from PIL import Image

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
    image = models.ImageField(verbose_name="Nuotrauka", upload_to="cars", null=True, blank=True)
    description = HTMLField(verbose_name="Aprašymas", max_length=5000, default="")

    class Meta:
        verbose_name = "Automobilis"
        verbose_name_plural = "Automobiliai"


    def __str__(self):
        return f"{self.car_model} ({self.licence_plate})"


class Order(models.Model):
    car = models.ForeignKey(to="Car", verbose_name="Automobilis", on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateTimeField(verbose_name="Data", auto_now_add=True)
    client = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, blank=True)
    deadline = models.DateTimeField(verbose_name="Gražinimo laikas", null=True, blank=True)

    def deadline_overdue(self):
        return self.status == "v" and self.deadline and self.deadline < timezone.now()

    # TODO total
    LOAN_STATUS = (
        ('p', 'Patvirtinta'),
        ('v', 'Vykdoma'),
        ('i', 'Įvykdyta'),
        ('a', 'Atšaukta'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default="p", help_text='Būsena')


    class Meta:
        verbose_name = "Užsakymas"
        verbose_name_plural = "Užsakymai"
        ordering = ['-id']

    def __str__(self):
        return f"{self.car} - {self.date}, total: {self.total()}"

    def total(self):
        return sum(line.line_sum() for line in self.lines.all())


class OrderLine(models.Model):
    order = models.ForeignKey(to="Order", verbose_name="Užsakymas", on_delete=models.CASCADE, related_name="lines")
    service = models.ForeignKey(to="Service", verbose_name="Paslauga", on_delete=models.SET_NULL, null=True, blank=True)
    qty = models.IntegerField(verbose_name="Kiekis", default=1)

    # TODO sum

    def line_sum(self):
        return self.service.price * self.qty

    class Meta:
        verbose_name = "Užsakymo eilutė"
        verbose_name_plural = "Užsakymo eilutės"

    def __str__(self):
        return f"{self.service} ({self.service.price}) * {self.qty} = {self.line_sum()} ({self.order.date})"


class OrderReview(models.Model):
    order = models.ForeignKey(to="Order", verbose_name="Užsakymas", on_delete=models.SET_NULL, null=True, blank=True, related_name="reviews")
    reviewer = models.ForeignKey(to=User, verbose_name="Komentatorius", on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateTimeField(verbose_name="Data", auto_now_add=True)
    content = models.TextField(verbose_name="Atsiliepimas", max_length=2000)

    class Meta:
        verbose_name = "Atsiliepimas"
        verbose_name_plural = 'Atsiliepimai'
        ordering = ['-date_created']


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(default="profile_pics/default.png", upload_to="profile_pics")

    def __str__(self):
        return f"{self.user.username} profilis"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.photo.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 3001)
            img.thumbnail(output_size)
            img.save(self.photo.path)