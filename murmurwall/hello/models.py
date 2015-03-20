from django.db import models

# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField('date created', auto_now_add=True)


# model to add in new word
class Word(models.Model):
    word = models.TextField()

    def __unicode__(self):
        return self.word
