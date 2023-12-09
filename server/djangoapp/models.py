from django.db import models
from django.utils.timezone import now



# Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)

    def __str__(self):
        return f"name: {self.name}, description: {self.description}"


# Car Model model `class CarModel(models.Model):`:
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
    COUPE = 'coupe'
    CABRIO = 'cabrio'

    CAR_TYPES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'Wagon'),
        (COUPE, 'Coupe'),
        (CABRIO, 'Cabrio')
    ]


    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    dealer_id = models.IntegerField()
    car_type = models.CharField(max_length=20, choices=CAR_TYPES, default=SEDAN)
    year = models.DateField()

    def __str__(self):
        return f"name:{self.name}  type:{self.car_type}  make:{self.car_make.name}"


# plain Python class `CarDealer` to hold dealer data
class CarDealer:

    def __init__(
        self, 
        address, 
        city, 
        full_name, 
        id, 
        lat, 
        long, 
        short_name, 
        st, 
        zip
    ):

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


# plain Python class `DealerReview` to hold review data
class DealerReview:

    def __init__(
        self, 
        dealership, 
        name, purchase, 
        review, 
        purchase_date,
        car_make, 
        car_model, 
        car_year, 
        sentiment, 
        id
    ):

        # Dealership name
        self.dealership = dealership
        # user name
        self.name = name
        # purchase
        self.purchase = purchase
        # review content
        self.review = review
        # purchase date
        self.purchase_date = purchase_date
        # car make
        self.car_make = car_make
        # car model
        self.car_model = car_model
        # car year
        self.car_year = car_year
        # sentiment
        self.sentiment = sentiment
        #id
        self.id = id