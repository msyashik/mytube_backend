from django.contrib import admin
from .models import Author

# Register your models here.
class AuthorAdmin(admin.ModelAdmin):
    fields = ["name", "email", "password"]
    list_display = ["name", "email"]

admin.site.register(Author, AuthorAdmin)
