from django.contrib import admin
from .models import Slider

# Register your models here.
class SliderAdmin(admin.ModelAdmin):
    list_display = ["__str__", "order", "start_date", "end_date", "active", "featured"]
    list_editable = ["order", "start_date", "end_date"]

    class Meta:
        model = Slider

admin.site.register(Slider, SliderAdmin)