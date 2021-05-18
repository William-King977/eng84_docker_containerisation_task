
from django.test import Client
import datetime

from django.test import TestCase
from ..models import Person, Staff, Passenger

# We will run tests for Person, Staff and Passenger
class PassengerTestCase(TestCase):

    # Let's define the objects that we will test if they have been added in the database
    def setUp(self):
        Person.objects.create(first_name="James" , last_name="Bond", dob="2019-05-06")
        Person.objects.create(first_name="John", last_name="Williams", dob="2020-03-06")

        Staff.objects.create(first_name="Lewis", last_name="Walker", dob="1996-10-12")
        Staff.objects.create(first_name="Carl", last_name="Maddison", dob="2000-03-30")

        Passenger.objects.create(first_name="Paul", last_name="Kane", dob="1994-06-14", passport_num="123456ABC")
        Passenger.objects.create(first_name="Jack", last_name="Rondon", dob="2010-04-08", passport_num="987654DEF")
        # Object to try to see what happens when we introduce two passengers with the same details
        # Passenger.objects.create(first_name="Paul", last_name="Kane", dob="1994-06-14", passport_num="123456ABC")
        # Object to try to see what happens when we introduce one passenger with a future day of birth
        # Passenger.objects.create(first_name="Paul", last_name="Kane", dob="2022-06-14", passport_num="123456ABC")

    # Function(test) to check if a passenger(parent_class) exists in the database
    def test_passenger(self):
        passenger1 = Passenger.objects.get(id=5)
        self.assertEqual(passenger1.first_name, "Paul")
        self.assertEqual(passenger1.last_name, "Kane")
        self.assertEqual(str(passenger1.dob), "1994-06-14")
        self.assertEqual(passenger1.passport_num, "123456ABC")
        passenger2 = Passenger.objects.get(id=6)
        self.assertEqual(passenger2.first_name, "Jack")
        self.assertEqual(passenger2.last_name, "Rondon")
        self.assertEqual(str(passenger2.dob), "2010-04-08")
        self.assertEqual(passenger2.passport_num, "987654DEF")

    # Function(test) to check if a person(parent_class) exists in the database    
    def test_person(self):
        person_test = Person.objects.get(id=1)
        person_test2 = Person.objects.get(id=2)
        self.assertEqual(person_test.first_name, "James")
        self.assertEqual(person_test.last_name, "Bond")
        self.assertEqual(str(person_test.dob), "2019-05-06")
        self.assertEqual(person_test2.first_name, "John")
        self.assertEqual(person_test2.last_name, "Williams")
        self.assertEqual(str(person_test2.dob), "2020-03-06")

    # Function(test) to check if a staff(children_class) exists in the database  
    def test_staff(self):
        staff1 = Staff.objects.get(id=3)
        self.assertEqual(staff1.first_name, "Lewis")
        self.assertEqual(staff1.last_name, "Walker")
        self.assertEqual(str(staff1.dob), "1996-10-12")
        staff2 = Staff.objects.get(id=4)
        self.assertEqual(staff2.first_name, "Carl")
        self.assertEqual(staff2.last_name, "Maddison")
        self.assertEqual(str(staff2.dob), "2000-03-30")

     
    # Function(test) to check if a passenger with a day of birth in the future has been added in the database
    def test_bod(self):
        person_test = Passenger.objects.get(id=5)
        today = datetime.date.today()
        date1 = today.strftime("%Y-%m-%d")
        self.assertLessEqual(str(person_test.dob), date1)
    

    # Function to check if the url of passenger is working
    def test_flight_url(self):
        client = Client()
        response = client.get("/passengers/")
        self.assertEqual(response.status_code, 200)

