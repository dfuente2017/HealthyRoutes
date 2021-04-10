from django.db import models

# Create your models here.

class User(models.Model):
    #nick = models.CharField(max_length = 10, required = True, null =False)
    #email = models.EmailField(max_length = 10, required = True, null =False)
    #password = models.CharField(min_length = 0, max_length = 10, required = True, null =False)
    nick = models.CharField(max_length = 10)
    email = models.EmailField()
    password = models.CharField(max_length = 10)

    def __str__(self):
        return self.nick + " " + self.email + " " + self.password