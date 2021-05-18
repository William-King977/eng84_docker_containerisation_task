from django.test import TestCase
import datetime
from django.test import Client
from ..models import Flight, Aircraft

# We will run tests for Flight
class FlightTestCase(TestCase):

    # Let's define the objects that we will test if they have been added in the database
    def setUp(self):
        Aircraft.objects.create(model="BOEING", manufacturer="Ryanair", capacity=100)
        aircraft1 = Aircraft.objects.get(aircraft_id=1)
        Flight.objects.create(origin="London", destination="Paris", departure_time="2022-04-13 18:35", duration="02:30", aircraft_id=aircraft1)
        # Object to try to see what happens when we introduce two passengers with the same details
        Flight.objects.create(origin="London", destination="Paris", departure_time="2022-04-13 18:35", duration="02:30", aircraft_id=aircraft1)
        # Object to try to see what happens when we introduce a flight with a past current day
        Flight.objects.create(origin="Paris", destination="Madrid", departure_time="2025-04-13 18:35", duration="03:35",aircraft_id=aircraft1)

    # Function(test) to check if a Flight(parent_class) exists in the database
    def test_flight(self):
        flight1 = Flight.objects.get(flight_id=1)
        aircraft1 = Aircraft.objects.get(aircraft_id=1)
        self.assertEqual(flight1.origin, "London")
        self.assertEqual(flight1.destination, "Paris")
        self.assertEqual(str(flight1.departure_time), "2022-04-13 18:35:00+00:00")
        self.assertEqual(str(flight1.duration), "02:30:00")
        self.assertEqual(flight1.aircraft_id, aircraft1)
        flight2 = Flight.objects.get(flight_id=2)
        self.assertEqual(flight2.origin, "London")
        self.assertEqual(flight2.destination, "Paris")
        self.assertEqual(str(flight2.departure_time), "2022-04-13 18:35:00+00:00")
        self.assertEqual(str(flight2.duration), "02:30:00")
        self.assertEqual(flight2.aircraft_id, aircraft1)

    # Function(test) to check if a flight with a past date has been inserted in the database
    def test_bod(self):
        flight_test = Flight.objects.get(flight_id=3)
        today = datetime.date.today()
        date1 = today.strftime("%Y-%m-%d")
        self.assertGreaterEqual(str(flight_test.departure_time), date1)

    # Function to check if the url of flights is working
    def test_flight_url(self):
        client = Client()
        response = client.get("/flights/")
        self.assertEqual(response.status_code, 200)
