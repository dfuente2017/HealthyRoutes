from djongo import models

# Create your models here.

class MessuresQuality(models.Model):
    id = models.ObjectIdField()
    messure_name = models.CharField(max_length = 15, blank = False, null = False)
    very_good = models.IntegerField(blank = False, null = False)
    good = models.IntegerField(blank = False, null = False)
    mediocre = models.IntegerField(blank = False, null = False)
    bad = models.IntegerField(blank = False, null = False)
    very_bad = models.IntegerField(blank = False, null = False)


class Messures(models.Model):
    id = models.ObjectIdField()
    so2_messure = models.DecimalField(max_digits = 7, decimal_places = 2, null = True)      #Dioxido de azufre      -> 1
    co_messure = models.DecimalField(max_digits = 7, decimal_places = 2, null = True)       #Monoxido de carbono    -> 6
    no_messure = models.DecimalField(max_digits = 7, decimal_places = 2, null = True)       #Monoxido de nitrogeno  -> 7
    no2_messure = models.DecimalField(max_digits = 7, decimal_places = 2, null = True)      #Dioxido de nitrogeno   -> 8
    pm2_5_messure = models.DecimalField(max_digits = 7, decimal_places = 2, null = True)    #PM2.5                  -> 9
    pm10_messure = models.DecimalField(max_digits = 7, decimal_places = 2, null = True)     #PM10                   -> 10
    nox_messure = models.DecimalField(max_digits = 7, decimal_places = 2, null = True)      #Oxidos de nitrogeno    -> 12
    o3_messure =  models.DecimalField(max_digits = 7, decimal_places = 2, null = True)      #Ozono                  -> 14
    tol_messure = models.DecimalField(max_digits = 7, decimal_places = 2, null = True)      #Tolueno                -> 20
    btx_messure = models.DecimalField(max_digits = 7, decimal_places = 2, null = True)      #Benceno                -> 30
    ebe_messure = models.DecimalField(max_digits = 7, decimal_places = 2, null = True)      #Etilbenceno            -> 35
    mxy_messure = models.DecimalField(max_digits = 7, decimal_places = 2, null = True)      #Metaxileno             -> 37
    pxy_messure = models.DecimalField(max_digits = 7, decimal_places = 2, null = True)      #Paraxileno             -> 38
    oxy_messure = models.DecimalField(max_digits = 7, decimal_places = 2, null = True)      #Ortoxileno             -> 39
    tch_messure = models.DecimalField(max_digits = 7, decimal_places = 2, null = True)      #Hidrocarburos totales  -> 42        
    ch4_messure = models.DecimalField(max_digits = 7, decimal_places = 2, null = True)      #Metano                 -> 43
    nmhc_messure = models.DecimalField(max_digits = 7, decimal_places = 2, null = True)     #Hidrocarburos no metánicos -> 44


class AirStation(models.Model):
    id = models.IntegerField(primary_key = True)
    name = models.CharField(max_length = 30, blank = False, null = True)
    town_id = models.IntegerField(blank = False, null = False)
    latitude = models.DecimalField(blank = False, max_digits=20, decimal_places=18)
    longitude = models.DecimalField(blank = False, max_digits=20, decimal_places=18)
    messures = models.EmbeddedField(model_container = Messures)
    air_quality = models.PositiveSmallIntegerField(null = True)     #5-> very good, 4-> good, 3-> mediocre, 2->bad, 1->very bad            null = True
    #town = models.ForeignKey(Province, on_delete=models.CASCADE)


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