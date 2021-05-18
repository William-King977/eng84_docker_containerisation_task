from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.models import AbstractBaseUser, UserManager, User


class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    dob = models.DateField()
    age = models.FloatField(blank=True, null=True)
    # ticket_number = models.IntegerField((), unique=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Staff(User): 
    PILOT = "PILOT"
    FLIGHT_ATTENDANT = "FLIGHT ATTENDANT"
    TICKET_AGENT = "TICKET AGENT"
    ADMIN= "ADMIN"


    ROLES = [
            (PILOT, _('Pilot')),
            (FLIGHT_ATTENDANT, _('Flight Attendant')),
            (TICKET_AGENT, _('Ticket Agent')),
            (ADMIN, _('Admin')),
            ]
 
    dob = models.DateField()
    role = models.CharField(max_length=30, choices=ROLES)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def get_absolute_url(self):
        return reverse("staff_detail", args=[str(self.pk)])



# Note: Renamed from User to avoid conflicts
class Passenger(Person):
    """
    Class that defines the passenger users.
    """
    passport_num = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def get_absolute_url(self):
        return reverse("passenger_detail", args=[str(self.pk)])


class Flight(models.Model):
    DEPARTURE = "DEPARTURE"
    ARRIVAL = "ARRIVAL"
    FLIGHT_TYPE = [
            (DEPARTURE, _('Departure')),
            (ARRIVAL, _('Arrival'))
            ]
    """
    Class that defines the model for a flight
    """
    flight_id = models.AutoField(primary_key=True)
    origin = models.ForeignKey('Airport', on_delete=models.CASCADE, related_name='origin', blank=True)
    destination = models.ForeignKey('Airport', on_delete=models.CASCADE, related_name='destination', blank=True)
    flight_type = models.CharField(max_length=30, choices=FLIGHT_TYPE)
    departure_time = models.DateTimeField('Departure Time')
    duration = models.TimeField('Duration', blank=True)
    aircraft_id = models.ForeignKey('Aircraft', on_delete=models.CASCADE)
    attendance = models.ManyToManyField(Passenger )
    crew = models.ManyToManyField(Staff)

    # Method that finds the url of a particular flight, given its id
    def get_absolute_url(self):
        return reverse('flight_detail', args=[str(self.flight_id)])

    # Method that makes the flight look pretty when printed (made into string)
    def __str__(self):
        try:
            return f"Flight from {self.origin} to {self.destination}"
        except ObjectDoesNotExist:
            return f"Prospective flight {self.flight_id}"


class Aircraft(models.Model):
    """
    Class that holds the type of aircraft
    """
    aircraft_id = models.AutoField(primary_key=True, null=False, blank=False)
    model = models.CharField(max_length=10)
    manufacturer = models.CharField(max_length=20)
    capacity = models.IntegerField()
    weight = models.IntegerField(default=50000)

    def __str__(self):
        return f'{self.model} no{self.aircraft_id} by {self.manufacturer}'

    def get_absolute_url(self):
        return reverse("aircraft_details", args=[str(self.aircraft_id)])


class Airport(models.Model):
    """ Class that holds the information about an airport """
    name = models.CharField(max_length=30, unique=True)
    city = models.CharField(max_length=30)
    country = models.CharField(max_length=30)
    distance = models.FloatField()

    def __str__(self):
        return f'{self.name} {self.city}, {self.country}'



# class Terminal:
#     def __init__(self, name_terminal):
#         self.name_terminal = name_terminal
# 
# 

