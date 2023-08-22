from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Chat(models.Model): # "models.Model" is used to define your own model classes (Models are basically tables (So I'm essentially creating a table called "Chat"))
    user = models.ForeignKey(User, on_delete=models.CASCADE) # When the user is deleted all associated data to the user will also be deleted
    message = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.message}'
    
# Making migrations in Django means saving and applying changes to your database (Models)
# Any change must be migrated
# python3 manage.py makemigrations --> python3 manage.py migrate