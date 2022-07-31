from django.contrib import admin
from .models import product, category, Opinion, report, brand, discount


# Register your models here.
class filterr(admin.ModelAdmin):
    list_display = ('title', 'text_area', 'name', 'id',)


class filterr2(admin.ModelAdmin):
    list_display = ('text', 'id_c',)


class slugi(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

    actions = ['dis', 'no_dis']

    def dis(self, request, product):
        from math import ceil
        discount1 = int(str(discount.objects.all().first()))

        for pro in product:
            if pro.is_discount is False:
                pro.last_price = pro.price
                pro.save()
                multiplier = discount1 / 100.  # discount / 100 in python 3
                old_price = pro.price
                new_price = ceil(old_price - (old_price * multiplier))
                pro.price = new_price
                pro.is_discount = True
                pro.cent = discount1
                pro.save()

    discount2 = discount.objects.all().first()

    dis.short_description = 'Set ' + str(discount2) + ' discount'

    def no_dis(self, request, product):

        for pro in product:
            if pro.is_discount is True:
                pro.price = pro.last_price
                pro.is_discount = False
                pro.cent = 0
                pro.save()

    no_dis.short_description = 'finished discount'


admin.site.register(product, slugi)
admin.site.register(category)
admin.site.register(Opinion, filterr)
admin.site.register(report, filterr2)
admin.site.register(brand)
admin.site.register(discount)
