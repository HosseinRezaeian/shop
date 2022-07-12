from django.contrib import admin
from .models import product, category, Opinion, report


# Register your models here.
class filterr(admin.ModelAdmin):
    list_display = ('title', 'text_area', 'name', 'id',)


class filterr2(admin.ModelAdmin):
    list_display = ('text', 'id_c',)


admin.site.register(product)
admin.site.register(category)
admin.site.register(Opinion, filterr)
admin.site.register(report, filterr2)
