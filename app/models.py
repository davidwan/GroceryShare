from django.db import models

# Create your models here.

class User (models.Model):
    user = models.CharField(max_length=70)
    full_name = models.CharField(max_length=70)
    email = models.EmailField(unique=True)
    current_city = models.CharField(max_length = 70)
    current_location = models.CharField(max_length = 70)
    image = models.CharField(max_length = 70)

    def __unicode__(self):
        if (self.current_location == ''):
            return ('%s, %s') % (self.full_name, self.current_location)
        else:
            return ('%s, %s') % (self.full_name, self.current_city)

class Recipe (models.Model):
    recipe_name = models.CharField(max_length=1000, unique = True)
    recipe_url = models.CharField(max_length=1000)
    ingredients = models.CharField(max_length=1000)

    def __unicode__(self):
        return self.recipe_name

class User_Recipes (models.Model):
    user = models.ForeignKey(User)
    recipe_name = models.ForeignKey(Recipe)
    epoch = models.DateTimeField(auto_now_add = True)

    def __unicode__(self):
         return ('%s, %s') %(self.user, self.recipe_name)


