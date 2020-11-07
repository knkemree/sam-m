from django.contrib import admin
from .models import Slider
from django.utils.html import format_html

# Register your models here.
class SliderAdmin(admin.ModelAdmin):
    list_display = ['image_tag', "order", "start_date", "end_date", "active", "featured"]
    list_editable = ["order", "start_date", "end_date"]

    class Meta:
        model = Slider

    def image_tag(self,obj):
        return format_html('<img src="{0}" style="width: auto; height:45px;" />'.format(obj.image.url))

admin.site.register(Slider, SliderAdmin)