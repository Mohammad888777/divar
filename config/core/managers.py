from django.db import models

class CityManager(models.Manager):

    def get_queryset(self) :
        return super().get_queryset().prefetch_related("commerical_set").all()
    



class SmallCityManager(models.Manager):

    def get_queryset(self) :
        return super().get_queryset().select_related("city").prefetch_related("commerical").all()


class TagManger(models.Manager):

    def get_queryset(self) :
        return super().get_queryset().prefetch_related("tags").all()



class FeatureManger(models.Manager):

    def get_queryset(self) :
        return super().get_queryset().prefetch_related("features").all()


class SavedCommericalManger(models.Manager):
    
    def get_queryset(self) :

        return super().get_queryset().prefetch_related("saved").select_related("user").all()



class CommericalManger(models.Manager):

    def get_queryset(self) :
        return super().get_queryset().select_related("user","city").prefetch_related(
                        "saved",
                        "features",
                        "tags",
                        "commericalimage_set",
                        "thread_set"
                    ).all()
    