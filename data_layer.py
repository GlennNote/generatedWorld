import django, sys
import apps.generated_world.models as m

django.setup()

'''
TO RUN THIS FILE:
1) Start the Django Shell:
    
--> python manage.py shell

2) Load and run a file:

EXAMPLE 1
>>> exec(open('data_layer.py').read())

EXAMPLE 2
>>> exec(open('apps/generated_world/data_layer.py').read())

'''

# for club in m.Club.objects.all():
#     print('{} --> \t{}'.format(club.league.name, club.name))

# for league in m.League.objects.filter(sport__contains='ball'):
#     print('{} - {}'.format(league.sport, league.name))
#     for club in league.clubs.all():
#         print('\t{}'.format(club.name))

# for city in m.City.objects.filter(population__lt=15000).order_by('-population'):
#     print('{}\t{}'.format(city.population, city.name))

# for club in Club.objects.filter(memberships__person__last='Smith'):
#     print(club.name)
#     for membership in club.memberships.filter(person__last='Smith'):
#         print('\t{} {}'.format(membership.person.first, membership.person.last))

def return_capitals():
    for city in m.City.objects.filter(is_capital=1):
        print(city.name)

def cities_reverse_order_population():
    for city in m.City.objects.all().order_by('-population'):
        print("{} \t {}".format(city.name, city.population))

def return_leagues_for_sport(search):
    for league in m.League.objects.all().filter(sport__contains=search):
        print(league.name)

def club_name_contains_string(search):
    for club in m.Club.objects.all().filter(name__contains=search):
        print(club.name)

def company_name_does_not_contain(search):
    for company in m.Company.objects.exclude(name__contains=search):
        print(company.name)

def companies_income_under(income):
    for company in m.Company.objects.filter(net_income__lt=income).order_by("-net_income"):
        print("{} \t {}".format(company.name, company.net_income))

def give_streets_by_integer(street):
    for address in m.Address.objects.filter(street__contains=street):
        print(address.street)

def cities_pop_between_integers(mini,maxi):
    for city in m.City.objects.filter(population__lt=maxi,population__gt=mini).order_by("-population"):
        print("{} \t {}".format(city.name, city.population))

def cities_cardinal_direction(direction):
    for city in m.City.objects.filter(name__startswith=direction):
        print("{}".format(city.name))

def companies_by_association(association):
    for company in m.Company.objects.filter(name__endswith=association):
        print("{}".format(company.name))
