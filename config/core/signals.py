from django.db.models.signals import  post_save
from .models import Commerical,Tag


def auto_create_tag(sender,created,instance,**kwargs):
    if created:
        tag=Tag(
            tag_name=instance.parent.title
        )
        tag.save()
        tag2=Tag(
            tag_name=instance.parent.title+' '+instance.location.name
        )
        tag2.save()
    
post_save.connect(auto_create_tag,sender=Commerical)