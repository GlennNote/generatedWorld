from django.db import models

class Person(models.Model):
    first = models.CharField(max_length=64)
    last = models.CharField(max_length=64)
    gender = models.CharField(max_length=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class State(models.Model):
    name = models.CharField(max_length=64)
    abbreviation = models.CharField(max_length=2, unique=True)
    gdp = models.FloatField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Company(models.Model):
    name = models.CharField(max_length=64, unique=True)
    revenue = models.FloatField()
    operating_income = models.FloatField()
    net_income = models.FloatField()
    total_assets = models.FloatField()
    
    founded_on = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class League(models.Model):
    name = models.CharField(max_length=64, unique=True)
    sport = models.CharField(max_length=64)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class City(models.Model):
    name = models.CharField(max_length=64)
    zipcode = models.CharField(max_length=10, unique=True)
    population = models.IntegerField()
    is_capital = models.IntegerField(default=0)
    state = models.ForeignKey(State, related_name='cities', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Exchange(models.Model):
    name = models.CharField(max_length=64)
    address = models.CharField(max_length=64)
    city = models.ForeignKey(City, related_name='exchanges', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Department(models.Model):
    name = models.CharField(max_length=64)
    company = models.ForeignKey(Company, related_name='departments', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Club(models.Model):
    name = models.CharField(max_length=64)
    league = models.ForeignKey(League, related_name='clubs', on_delete=models.CASCADE)
    city = models.ForeignKey(City, related_name='clubs', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Membership(models.Model):
    is_active = models.IntegerField()
    club = models.ForeignKey(Club, related_name='memberships', on_delete=models.CASCADE)
    person = models.ForeignKey(Person, related_name='memberships', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Employment(models.Model):
    is_employed = models.IntegerField()
    department = models.ForeignKey(Department, related_name='employees', on_delete=models.CASCADE)
    person = models.ForeignKey(Person, related_name='jobs', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Listing(models.Model):
    symbol = models.CharField(max_length=5, unique=True)
    industry = models.CharField(max_length=64)
    company = models.ForeignKey(Company, related_name='listings', on_delete=models.CASCADE)
    exchange = models.ForeignKey(Exchange, related_name='listings', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Address(models.Model):
    street = models.CharField(max_length=128)
    is_current = models.IntegerField()
    person = models.ForeignKey(Person, related_name='addresses', on_delete=models.CASCADE)
    city = models.ForeignKey(City, related_name='addresses', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

