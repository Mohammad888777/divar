from django.contrib import admin
from .models import (
                Commerical,SavedCommerical
                ,SmallCity,City,Thread,
                Message,Feature,Tag,
                CommericalImage,Location
            )

class CommericalAdmin(admin.ModelAdmin):

    list_display=["title","parent","city","iranTimeCreated","price"]

admin.site.register(Commerical,CommericalAdmin)



admin.site.register([SavedCommerical,SmallCity,City,Thread,
                    Message,Feature,Tag,
                    CommericalImage,Location])
