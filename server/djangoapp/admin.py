from django.contrib import admin
from .models import CarMake, CarModel


# Register your models here.

# CarModelInline class
class CarModelInLine(admin.StackedInline):
    model = CarModel
    extra = 5

# CarModelAdmin class
admin.site.register(CarModel)

# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInLine]

admin.site.register(CarMake, CarMakeAdmin)

# Register models here
