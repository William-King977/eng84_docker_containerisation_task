from datetime import timedelta, datetime,date

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Person, Staff, Passenger, Flight, Aircraft, Airport
from .forms import FlightsForm, PassengerForm, StaffForm, AirportForm, AircraftForm

from .vars import AIRPLANE_SPEED
from .pricing import cost_of_flight
"""
           HOME-LOGIN
"""
# Login Page


class HomeView(ListView):
    template_name = 'home.html'
    context_object_name = 'queryset'

    # Overwrite default 'get_queryset' method to get all the objects in the database
    def get_queryset(self):
        # Write the queryset of each object as key-value pair and pass all of them as a dictionary object
        queryset = {
                'arrivals': Flight.objects.filter(flight_type__exact='ARRIVAL'),
                'departures': Flight.objects.filter(flight_type__exact='DEPARTURE'),
                }
        return queryset


class AirportAppLoginView(LoginView):
    template_name = 'login.html'


"""
            PASSENGERS
"""


# Passengers Page
class PassengerListView(LoginRequiredMixin, ListView):
    model = Passenger
    template_name = 'passengers.html'
    context_object_name = 'queryset'


class PassengerCreateView(LoginRequiredMixin, CreateView):
    model = Passenger
    template_name = "passenger_create.html"
    form_class = PassengerForm

    def form_valid(self, form):
        self.object = form.save(commit=False)

        date_of_birth = form.cleaned_data.get('dob')
        age = (date.today() - date_of_birth).days /364.25
        self.object.age = age
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class PassengerDetailView(LoginRequiredMixin, DetailView):
    model = Passenger
    template_name = 'passenger_detail.html'
    context_object_name = 'queryset'

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(*args, **kwargs)
        return data


class PassengerUpdateView(LoginRequiredMixin, UpdateView):
    model = Passenger
    template_name = 'passenger_update.html'
    form_class = PassengerForm

    def form_valid(self, form):
        self.object = form.save(commit=False)

        date_of_birth = form.cleaned_data.get('dob')
        age = (date.today() - date_of_birth).days /364.25
        self.object.age = age
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

class PassengerDeleteView(LoginRequiredMixin, DeleteView):
    model = Passenger
    template_name = 'passenger_confirm_delete.html'
    success_url = reverse_lazy('passengers')


"""
            FLIGHTS
"""


# Flights Page
class FlightListView(LoginRequiredMixin, ListView):
    model = Flight
    template_name = 'flights.html'
    context_object_name = 'queryset'


# Flights Detail Page
class FlightDetailView(LoginRequiredMixin, DetailView):
    model = Flight
    template_name = 'flight_detail.html'
    context_object_name = 'queryset'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Count available seats
        full_capacity = self.object.aircraft_id.capacity
        seats_taken = len(self.object.attendance.all()) + len(self.object.crew.all())
        available = full_capacity - seats_taken

        # Get price of flight

        distance = self.object.destination.distance + self.object.origin.distance
        cost = cost_of_flight(self.object.aircraft_id.weight, distance)

        price = 100

        payout = [price if passenger.age > 1 else 0 for passenger in self.object.attendance.all()]
        revenue = sum(payout)
        # Add to context
        context.update({
            'available': available,
            'cost': cost,
            'revenue': revenue,
            'payout': payout,
            })
        print(context)

        return context


class FlightCreateView(LoginRequiredMixin, CreateView):
    model = Flight
    template_name = 'flight_create.html'
    form_class = FlightsForm

    def form_valid(self, form):
        print("\n\nTEST\n\n\n")
        self.object = form.save(commit=False)
        distance = form.cleaned_data.get('connection').distance
        duration = distance / AIRPLANE_SPEED
        time = timedelta(hours = duration)
        self.object.duration = str(time)
        # Set destination / origin
        ft = form.cleaned_data.get('flight_type')

        if form.cleaned_data.get('flight_type') == "ARRIVAL":
            self.object.destination = Airport.objects.get(id=1)
            self.object.origin = form.cleaned_data.get('connection')
        else:
            self.object.origin = Airport.objects.get(id=1)
            self.object.destination = form.cleaned_data.get('connection')

        self.object.save()
        self.object.attendance.set(form.cleaned_data.get('attendance'))
        self.object.crew.set(form.cleaned_data.get('crew'))
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class FlightUpdateView(LoginRequiredMixin, UpdateView):
    model = Flight
    template_name = 'flight_update.html'
    form_class = FlightsForm

    def form_valid(self, form):
        print("\n\nTEST\n\n\n")
        self.object = form.save(commit=False)
        distance = form.cleaned_data.get('connection').distance
        duration = distance / AIRPLANE_SPEED
        time = timedelta(hours = duration)
        self.object.duration = str(time)
        # Set destination / origin
        ft = form.cleaned_data.get('flight_type')

        if form.cleaned_data.get('flight_type') == "ARRIVAL":
            self.object.destination = Airport.objects.get(id=1)
            self.object.origin = form.cleaned_data.get('connection')
        else:
            self.object.origin = Airport.objects.get(id=1)
            self.object.destination = form.cleaned_data.get('connection')

        self.object.save()
        self.object.attendance.set(form.cleaned_data.get('attendance'))
        self.object.crew.set(form.cleaned_data.get('crew'))
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class FlightDeleteView(LoginRequiredMixin, DeleteView):
    model = Flight
    template_name = 'flight_confirm_delete.html'
    success_url = reverse_lazy('flights')


"""
           AIRCRAFT
"""


class AircraftListView(LoginRequiredMixin, ListView):
    model = Aircraft
    template_name = 'aircrafts.html'
    context_object_name = 'queryset'


class AircraftCreateView(LoginRequiredMixin,CreateView):
    model = Aircraft
    template_name = 'aircraft_create.html'
    form_class = AircraftForm


class AircraftDetailView(LoginRequiredMixin, DetailView):
    model = Aircraft
    template_name = 'aircraft_details.html'
    context_object_name = 'queryset'


"""
           STAFF
"""


class StaffListView(LoginRequiredMixin, ListView):
    model = Staff
    template_name = 'staff_list.html'
    context_object_name = 'queryset'


class StaffCreateView(LoginRequiredMixin, CreateView):
    model = Staff
    template_name = "staff_create.html"
    form_class = StaffForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.username = form.cleaned_data.get('email')
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class StaffUpdateView(LoginRequiredMixin, UpdateView):
    model = Staff
    template_name = "staff_update.html"
    form_class = StaffForm


class StaffDetailView(LoginRequiredMixin, DetailView):
    model = Staff
    template_name = 'staff_detail.html'
    context_object_name = 'queryset'


class StaffDeleteView(LoginRequiredMixin, DeleteView):
    model = Staff
    template_name = 'staff_confirm_delete.html'
    success_url = reverse_lazy('staff_list')


"""
           AIRPORTS
"""


class AirportListView(LoginRequiredMixin, ListView):
    model = Airport
    template_name = 'airports.html'
    context_object_name = 'queryset'

    def get_queryset(self):
        # Write the queryset of each object as key-value pair and pass all of them as a dictionary object
        queryset = {
                'current': Airport.objects.filter(id__exact=1).first(),
                'other': Airport.objects.exclude(id__exact=1).all(),
                }
        return queryset


class AirportCreateView(LoginRequiredMixin, CreateView):
    model = Airport 
    template_name = "airport_create.html"
    form_class = AirportForm
    success_url = reverse_lazy('airports')


class AirportDetailView(LoginRequiredMixin, DetailView):
    model = Airport 
    template_name = 'staff_detail.html'
    context_object_name = 'queryset'
