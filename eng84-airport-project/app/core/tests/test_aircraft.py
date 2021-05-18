from django.test import TestCase
from django.test import Client
from ..models import Aircraft

# We will run tests for Aircraft
class AircraftTestCase(TestCase):

    # Let's define the objects that we will test if they have been added in the database
    def setUp(self):
        Aircraft.objects.create(model="BOEING", manufacturer="Ryanair", capacity=100)
        # Object to try to see what happens when we introduce two passengers with the same details
        # Aircraft.objects.create(model="BOEING", manufacturer="Ryanair", capacity=100)

    # Function(test) to check if a Aircraft(parent_class) exists in the database
    def test_aircraft(self):
        aircraft1 = Aircraft.objects.get(aircraft_id=1)
        self.assertEqual(aircraft1.model, "BOEING")
        self.assertEqual(aircraft1.manufacturer, "Ryanair")
        self.assertEqual(aircraft1.capacity, 100)
        '''
        aircraft2 = Aircraft.objects.get(aircraft_id=2)
        self.assertEqual(aircraft2.model, "BOEING")
        self.assertEqual(aircraft2.manufacturer, "Ryanair")
        self.assertEqual(aircraft2.capacity, 100)
        '''

    # Function to check if the url of aircrafts is working
    def test_flight_url(self):
        client = Client()
        response = client.get("/aircrafts/")
        self.assertEqual(response.status_code, 200)
