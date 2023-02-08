from django.db import models
class Employee(models.Model):
    name=models.CharField(max_length=100,null=False)
    email=models.CharField(max_length=50,null=False)
    salary=models.IntegerField()
    def __str__(self):
        return self.name