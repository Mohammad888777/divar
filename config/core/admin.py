from django.contrib import admin
from .models import (
                Commerical,SavedCommerical
                ,SmallCity,City,Thread,
                Message,Feature,Tag,
                CommericalImage,Location
            )

class CommericalAdmin(admin.ModelAdmin):

    list_display=[

        "title","parent","city","iranTimeCreated",
        "price",'com_status','location',
        'publisher','ready_to_exchange','phone_status',
        'publisherForCar',
        'bg_red_for_cars','yellow_red_for_phones',
        'all_parents'
    ]
    search_fields=["title"]
    

admin.site.register(Commerical,CommericalAdmin)



admin.site.register([SavedCommerical,SmallCity,City,Thread,
                    Message,Feature,Tag,
                    CommericalImage,Location])
