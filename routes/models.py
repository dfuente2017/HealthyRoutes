from djongo import models

# Create your models here.

class Node(models.Model):
    id = models.ObjectIdField()
    latitude = models.DecimalField(max_digits=18, decimal_places=15, null= True)
    longitude = models.DecimalField(max_digits=18, decimal_places=15, null = True)
    air_quality = models.IntegerField(null = True)
    surface_quality = models.BooleanField(null = True)


class Instruction(models.Model):
    id = models.ObjectIdField()
    distance = models.DecimalField(max_digits=5, decimal_places=2, null= True)        #Cambiar a number
    text = models.CharField(max_length=50, null = True)


class Route(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    user = models.EmailField(max_length = 60, null = False)
    date_saved = models.DateTimeField(auto_now = True, null = False)
    distance = models.DecimalField(max_digits=5, decimal_places=2, null= False)
    time = models.IntegerField(null= False)
    instructions = models.ArrayField(model_container = Instruction, null = True)
    nodes = models.ArrayField(model_container = Node, null= False)

    #Percentage of nodes with each air quality
    very_good_air_quality_nodes = models.IntegerField(null = False)
    good_air_quality_nodes = models.IntegerField(null = False)
    mediocre_air_quality_nodes = models.IntegerField(null = False)
    bad_air_quality_nodes = models.IntegerField(null = False)
    very_bad_air_quality_nodes = models.IntegerField(null = False)
    unknown_air_quality_nodes = models.IntegerField(null = False)

    ranking_puntuation = models.DecimalField(max_digits=4, decimal_places=1, null = False)