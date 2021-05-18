from django.conf import settings
from django.urls import path
from . import views
from django.conf.urls.static import static

from .views import (HomeView, FlightListView, PassengerListView, FlightDetailView, FlightCreateView,
                    FlightUpdateView, FlightDeleteView, AircraftListView, AircraftCreateView, PassengerCreateView, PassengerDetailView,
                    AircraftDetailView, AirportAppLoginView, StaffCreateView, StaffDetailView, StaffListView,
                    StaffUpdateView, StaffDeleteView, LogoutView, PassengerDeleteView, PassengerUpdateView,
                    AirportCreateView, AirportDetailView, AirportListView,
                    )

urlpatterns = [
        path('', HomeView.as_view(), name='index'),
        path('home/', HomeView.as_view(), name='index'),
        path('login/', AirportAppLoginView.as_view(), name='login'),
        path('logout/', LogoutView.as_view(), name='logout'),
        path('flights/', FlightListView.as_view(), name='flights'),
        path('passengers/', PassengerListView.as_view(), name='passengers'),
        path('add_passenger/', PassengerCreateView.as_view(), name='add_passengers'),
        path('passengers/<int:pk>', PassengerDetailView.as_view(), name='passenger_detail'),
        path('passengers/<int:pk>/update', PassengerUpdateView.as_view(), name='passenger_update'),
        path('passengers/<int:pk>/delete', PassengerDeleteView.as_view(), name='passenger_delete'),
        path('flights/<int:pk>', FlightDetailView.as_view(), name='flight_detail'),
        path('flights/create', FlightCreateView.as_view(), name='flight_create'),
        path('flights/<int:pk>/update', FlightUpdateView.as_view(), name='flight_update'),
        path('flights/<int:pk>/delete', FlightDeleteView.as_view(), name='flight_delete'),
        path('aircrafts/', AircraftListView.as_view(), name='aircrafts'),
        path('aircrafts/<int:pk>', AircraftDetailView.as_view(), name='aircraft_details'),
        path('aircrafts/create', AircraftCreateView.as_view(), name='aircraft_create'),
        path('staff/', StaffListView.as_view(), name='staff_list' ),
        path('staff/<int:pk>', StaffDetailView.as_view(), name='staff_detail' ),
        path('staff/create', StaffCreateView.as_view(), name='staff_create' ),
        path('staff/<int:pk>/edit', StaffUpdateView.as_view(), name='staff_update' ),
        path('staff/<int:pk>/delete', StaffDeleteView.as_view(), name='staff_delete' ),
        path('airports/', AirportListView.as_view(), name='airports' ),
        path('airports/create', AirportCreateView.as_view(), name='airport_create' ),
        #path('airports/<int:pk>', AirportDetailView.as_view(), name='airport_detail' ),
        ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
