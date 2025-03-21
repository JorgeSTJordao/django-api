from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=200)
    age = models.IntegerField()
    ssn = models.CharField(max_length=100)

    # User is equivalent to this through this function
    def __str__(self):
        return self.name
        
        
