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
    distance = models.DecimalField(max_digits=18, decimal_places=15, null= True)        #Cambiar a number
    text = models.CharField(max_length=50, null = True)


class Route(models.Model):
    id = models.IntegerField(primary_key = True)
    user = models.EmailField(max_length = 60, null = True)
    distance = models.DecimalField(max_digits=18, decimal_places=15, null= True)
    time = models.IntegerField(null= True)
    instructions = models.ArrayField(model_container = Instruction, null = True)
    nodes = models.ArrayField(model_container = Node, null= True)
    ranking_puntuation = models.DecimalField(max_digits=18, decimal_places=15, null = True)