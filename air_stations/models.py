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



"""def migracion():
    antiguos_argumentos = FactoryReadCsvArguments.objects.all()
    antiguos_argumentos = antiguos_argumentos[0]

    nuevos_argumentos = Arguments.objects.create(town_id = 79, argument_type = 'ASD', arguments = antiguos_argumentos.arguments)
    nuevos_argumentos.save()"""

"""def aux():
    arguments_list = [{'id':0,'argument':'Dato_Horario'},{'id':1,'argument':'municipio'},{'id':2,'argument':'estacion'},{'id':3,'argument':'magnitud'},{'id':4,'argument':'H##'},{'id':5,'argument':'V##'},]
    Arguments.objects.create(town_id = 79, argument_type = 'AMD', arguments = arguments_list)

def aux1():
    arguments_list = [{'id':0, 'argument':'CODIGO'},{'id':1, 'argument':'ESTACION'},{'id':2, 'argument':'LONGITUD'},{'id':3, 'argument':'LATITUD'},]
    Arguments.objects.create(id = 1, town_id = 79, argument_type = 'ASD', arguments = arguments_list)"""