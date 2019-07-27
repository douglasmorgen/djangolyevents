from django.db import models

# Create your models here.
class Event(models.Model):

    eventname=models.CharField(max_length=255)
    date = models.DateTimeField()
    def __str__(self):
        return "%s %s" % (self.eventname,self.date)