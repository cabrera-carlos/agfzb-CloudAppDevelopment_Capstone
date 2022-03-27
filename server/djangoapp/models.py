from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=250)

    def __str__(self):
        return "Name: " + self.name + "," + \
               "Description: " + self.description


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    SEDAN = 'sedan'
    SUV = 'suv'
    WAGON = 'wagon'
    PICKUP = 'pickup'
    VAN = 'van'
    MINIVAN = 'minivan'
    SPORT = 'sport'
    
    types = [
        (SEDAN, 'sedan')
        , (SUV, 'suv')
        , (WAGON, 'wagon')
        , (PICKUP, 'pickup')
        , (VAN, 'van')
        , (MINIVAN, 'minivan')
        , (SPORT, 'sport')
    ]

    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    dealer_id = models.IntegerField()
    type = models.CharField(max_length=50, choices=types, default=SEDAN)
    year = models.DateField()

    def __str__(self):
        return "Name: " + self.name + "," + \
            "Description: " + self.type + \
            "Description: " + str(self.year)


# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    # Sentiment analysis score
    sentiment =  None
    
    # Optional fields
    purchase_date = None
    car_make = None
    car_model = None
    car_year = None

    def __init__(self, dealership, name, purchase, review, id):
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        self.id = id

    def __str__(self):
        return "Reviewer Name: " + self.name + \
            "Review: " + self.review

