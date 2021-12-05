from djongo import models

#from djangotoolbox.fields import ListField, EmbeddedModelField

# Create your models here.

class Messures(models.Model):
    id = models.ObjectIdField()
    no2_messure = models.IntegerField(null = True)      #Dioxido de nitrogeno   -> 7
    so2_messure = models.IntegerField(null = True)      #Dioxido de azufre      -> 1 
    co_messure = models.IntegerField(null = True)       #Monoxido de carbono    -> 6
    pm10_messure = models.IntegerField(null = True)     #PM10                   -> 10
    pm2_5_messure = models.IntegerField(null = True)    #PM2.5                  -> 9
    o3_messure =  models.IntegerField(null = True)      #Ozono                  -> 14
    btx_messure = models.IntegerField(null = True)      #Benceno                -> 30

class AirStation(models.Model):
    id = models.IntegerField(primary_key = True)
    name = models.CharField(max_length = 30, blank = False, null = True)
    latitude = models.DecimalField(blank = False, max_digits=20, decimal_places=18)
    longitude = models.DecimalField(blank = False, max_digits=20, decimal_places=18)
    messures = models.EmbeddedField(model_container = Messures)


"""It is important to assing last_modified a date with datetime format, and previous or equal to the actual time."""
class Town(models.Model):
    id = models.IntegerField(primary_key = True)
    name = models.CharField(max_length = 30, null = True)
    air_stations = models.ArrayField(model_container = AirStation)
    url = models.URLField()
    last_modified = models.DateTimeField(auto_now_add=True, null = True)
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

class Argument(models.Model):
    id = models.IntegerField(primary_key = True)
    argument = models.CharField(max_length = 30, null = True)

class Arguments(models.Model):
    ARGUMENT_SIZE = [
        ('ASD','Air Stations Data'),
        ('AMD','Air Messures Data'),
    ]

    id = models.IntegerField(primary_key = True)
    town_id = models.IntegerField(null = False)
    argument_type = models.CharField(max_length = 30, null = False)
    arguments = models.ArrayField(model_container = Argument)