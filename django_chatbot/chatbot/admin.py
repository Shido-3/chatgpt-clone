from django.contrib import admin
from .models import Chat # ".models" is where all our models (tables) are stored "Chat" is the specific table we would like to import

# Register your models here.
admin.site.register(Chat) # Registers "Chat" as a database