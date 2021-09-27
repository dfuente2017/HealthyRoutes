from djongo import models

#from djangotoolbox.fields import ListField, EmbeddedModelField

# Create your models here.

class Messures(models.Model):
    id = models.IntegerField(primary_key = True)
    no2_messure = models.IntegerField(blank = True)
    so2_messure = models.IntegerField(blank = True)
    co_messure = models.IntegerField(blank = True)
    pm10_messure = models.IntegerField(blank = True)
    pm2_5_messure = models.IntegerField(blank = True)
    o3_messure =  models.IntegerField(blank = True)
    btx_messure = models.IntegerField(blank = True)

class AirStation(models.Model):
    id = models.IntegerField(primary_key = True)
    name = models.CharField(max_length = 30, blank = False, null = True)
    latitude = models.DecimalField(blank = False, max_digits=20, decimal_places=18)
    longitude = models.DecimalField(blank = False, max_digits=20, decimal_places=18)
    messures = models.EmbeddedField(model_container = Messures)

class Town(models.Model):
    id = models.IntegerField(primary_key = True)
    name = models.CharField(max_length = 30, null = True)
    air_stations = models.ArrayField(model_container = AirStation)
    url = models.URLField()
    province = models.IntegerField(null = True)
    #province = models.ForeignKey(Province, on_delete=models.CASCADE)

class Province(models.Model):
    id = models.IntegerField(primary_key = True)
    name = models.CharField(max_length = 30, null = True)
    country = models.IntegerField(null = True)
    #country = models.ForeignKey(Country, on_delete = models.CASCADE)

class Country(models.Model):
    id = models.IntegerField(primary_key = True)
    name = models.CharField(max_length = 30)

class Arguments(models.Model):
    id = models.IntegerField(primary_key = True)
    argument = models.CharField(max_length = 30, null = True)

class FactoryReadCsvArguments(models.Model):
    town_id = models.IntegerField(primary_key = True)
    arguments = models.ArrayField(model_container = Arguments)