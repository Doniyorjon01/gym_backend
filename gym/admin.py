from django.contrib import admin
from . import models

class SportTypeAdmin(admin.ModelAdmin):
    fields = ['id', 'name']
    list_display = ('id', 'name',)
    search_fields = ('name',)
    list_filter = ('name',)
    readonly_fields = ('id', )


class LocationAdmin(admin.ModelAdmin):
    fields = ('address',)
    list_display = ('address',)
    search_fields = ('address',)
    list_filter = ('address',)
    readonly_fields = ('created_by', 'updated_by')


class GymAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'location', 'open_time', 'close_time', 'owner', 'trainers_list',
                    'image_file', 'image', 'phone_number', 'price', 'three_month_discount_price',
                    'six_month_discount_price', 'twelve_month_discount_price')
    search_fields = ('name', 'price', 'location', 'owner', 'trainers')
    list_filter = ('name', 'price', 'location', 'owner', 'trainers')
    fields = ('name', 'description', 'location', 'open_time', 'close_time', 'owner', 'trainers',
                    'image_file', 'image', 'phone_number', 'price', 'three_month_discount_price',
                    'six_month_discount_price', 'twelve_month_discount_price')

    def trainers_list(self, obj):
        return ", ".join([trainer.username for trainer in obj.trainers.all()])
    trainers_list.short_description = 'Trainers'


admin.site.register(models.SportType, SportTypeAdmin)
admin.site.register(models.Location, LocationAdmin)
admin.site.register(models.Gym, GymAdmin)


