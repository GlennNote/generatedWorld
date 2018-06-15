import django, sys
import apps.generated_world.models as m
from django.db.models import Count, Sum, Max
from django.utils.dateparse import parse_date

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

##########################################################################################

def companies_that_have_department(search):
    for department in m.Department.objects.filter(name__contains=search):
        print("{} has {} department.".format(department.company.name, search))

def all_people_currently_employed():
    for employment in m.Employment.objects.filter(is_employed=1):
        print(employment.person.first, employment.person.last)

def people_playing_for_club(search):
    for person in m.Person.objects.filter(memberships__is_active=1, memberships__club__name=search):
        print(person.first, person.last)
        
def find_all_past_addresses(person_first, person_last):
    for address in m.Address.objects.filter(is_current=0, person__first=person_first, person__last=person_last):
        print(address.street)  

def find_companies_for_industry(industry):
    for listed_company in m.Listing.objects.filter(industry__contains=industry):
        print(listed_company.company.name)

def find_clubs_in_league(search):
    for club in m.Club.objects.filter(league__name=search):
        print(club.name)

def find_state_with_most_cities():
    for state in m.State.objects.annotate(count=Count('cities')).order_by('-count'):
        print("{} -- {}".format(state.name, state.count))
        
# 8. Finds the most populous state
def find_state_with_most_people():
    state = m.State.objects.annotate(total_population=Sum("cities__population")).order_by("-total_population").first()
    print("{} == {}".format(state.name, state.total_population))
        
# 9. Finds the total assets for a given industry
def total_assets_for_industry(search):
    industry_total = m.Listing.objects.filter(industry__contains=search).aggregate(total_assets_industry=Sum("company__total_assets"))
    print(industry_total)

# 10. Find the companies for a given industry after a certain date
def companies_in_industry_after_date(industry_search, date_search):
    for company in m.Company.objects.filter(listings__industry__contains=industry_search, founded_on__gt=date_search):
        print(company.name)

##################### FUCK YEAH ###############################################################################3

# 1. Returns the states in descending order by the number of cities they have
def states_desc_number_cities():
    for state in m.State.objects.annotate(total_cities=Count("cities")).order_by("-total_cities"):
        print("{} \t {}".format(state.name, state.total_cities))

# 2. Returns the clubs that have the most past memberships
def clubs_with_most_past_memberships():
    for club in m.Club.objects.filter(memberships__is_active=0).annotate(total_past_members=Count("memberships__club")).order_by('-total_past_members')[:10]:
        print(club.total_past_members)

# 3. Returns the exchanges in descending order by the number of listings they have
def exchanges_desc_number_of_listings():
    for exchange in m.Exchange.objects.annotate(number_of_listings=Count("listings")).order_by("-number_of_listings"):
        print(exchange.number_of_listings)

# 4. Returns the companies with the most number of departments
def companies_with_most_departments():
    for company in m.Company.objects.annotate(number_of_departments=Count("departments")).order_by('-number_of_departments')[:20]:
        print(company.number_of_departments)

# 5. Returns the cities with the most employed people
def cities_with_most_employed_people():
    for city in m.City.objects.filter(addresses__person__jobs__is_employed=1).annotate(number_of_employed=Count("addresses__person__jobs")).order_by('-number_of_employed')[:25]:
        print("{} :: {} ".format(city.name, city.number_of_employed))

# 6. Returns the most profitable industries ============================================================================
def most_profitable_industries():
    for listing in m.Listing.objects.annotate(profit_per_industry=Sum("company__net_income")).order_by("industry"):
        print("{} :: {}".format(listing.industry, listing.profit_per_industry))

# 7. Returns the leagues in order of past membership
def leagues_in_order_of_past_membership():
    for league in m.League.objects.filter(clubs__memberships__is_active=0).annotate(past_membership=Count("clubs__memberships__is_active")).order_by('-past_membership'):
        print("{} :: {}".format(league.name, league.past_membership))


# 8. Returns the industries with the highest rate of unemployment
def industries_by_unemployment():
    for listing in m.Listing.objects.filter(company__departments__employees__is_employed=0).annotate(unemployed_count=Count("company__departments__employees__is_employed")).order_by("-unemployed_count"):
        print("{} :: {}".format(listing.industry, listing.unemployed_count))


# 9. Returns the cities with the most vacant addresses
def cities_with_most_vacant_addresses():
    for city in m.City.objects.filter(addresses__is_current=0).annotate(vacant_addresses=Count("addresses__is_current")).order_by("-vacant_addresses"):
        print("{} :: {}".format(city.name, city.vacant_addresses))

# 10. Returns the states in descending order by revenue
def return_states_desc_by_revenue():
    for state in m.State.objects.annotate(state_revenue=Sum("cities__exchanges__listings__company__revenue")).order_by('-state_revenue'):
        print("{} :: {}".format(state.name, state.state_revenue))

return_states_desc_by_revenue()