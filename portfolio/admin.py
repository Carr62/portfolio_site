from django.contrib import admin
from .models import Home, About, ContactMessage, Project
# Register your models here.

admin.site.register(Home)
admin.site.register(About)
admin.site.register(ContactMessage)
admin.site.register(Project)