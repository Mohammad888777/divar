from django.db import models
from accounts.models import User
from django.core.validators import FileExtensionValidator
from jalali_date import datetime2jalali, date2jalali
from django.utils import timezone
from .managers import (CityManager,
                       TagManger,FeatureManger,SavedCommericalManger,
                       CommericalManger
                       )
from django.utils.html import format_html

from .utilty import (   
                        BODY_STATUS,COMMERICAL_STATUS,
                        FUEL_CHOICES,
                        PUBLISHER_CHOICES,ORIGINAL_OR_NOT,
                        ENGIN_TYPE,PHONE_STATUS,TRANSMITION_TYPE,
                        RENT_STATUS,PUBLISHERForCar_CHOICES,COVERSIMCART,COLORS,
                        INTERNALOREXTERNAL,MEMORYSIZE,SIMCARTTYPE,CLOSTHTYPE
                     )





class City(models.Model):

    name=models.CharField(max_length=200)
    objects=CityManager()

    def __str__(self) -> str:
        return self.name


class Location(models.Model):

    name=models.CharField(max_length=200,null=True,blank=True)
    location_nickName=models.CharField(max_length=200,null=True,blank=True)
    city=models.ForeignKey(City, on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return self.name
    





class SmallCity(models.Model):

    city=models.ForeignKey(City,on_delete=models.CASCADE)
    name=models.CharField(max_length=200)

 

    def __str__(self) -> str:
        return self.name
    


class Tag(models.Model):

    tag_name=models.CharField(max_length=200)
    objects=TagManger()

    def __str__(self) -> str:
        return self.tag_name

class Feature(models.Model):

    name=models.CharField(max_length=200)
    # objects=FeatureManger()

    def __str__(self) -> str:
        return self.name


class SavedCommerical(models.Model):

    user=models.ForeignKey(User,on_delete=models.CASCADE)


    # objects=SavedCommericalManger()





class Commerical(models.Model):


    title=models.CharField(max_length=50)
    tags=models.ManyToManyField(Tag,related_name="tags")
    saved=models.ManyToManyField(SavedCommerical,related_name="saved")
    features=models.ManyToManyField(Feature,related_name="features")
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="user",null=True,blank=True)
    ready_to_exchange=models.BooleanField(default=False)
    parent=models.ForeignKey("self",on_delete=models.CASCADE,null=True,blank=True,related_name="+")
    location=models.ForeignKey(Location, on_delete=models.CASCADE,null=True,blank=True)
    smallCity=models.ForeignKey(SmallCity, on_delete=models.CASCADE,null=True,blank=True)

    # املاکککککککک
    city=models.ForeignKey(City,on_delete=models.CASCADE,null=True,blank=True)

    meter=models.IntegerField(null=True,blank=True)
    year_of_construction=models.IntegerField(null=True,blank=True)
    rooms=models.IntegerField(null=True,blank=True) 
    price=models.IntegerField(null=True,blank=True)
    price_each_meter=models.IntegerField(null=True,blank=True)
    vadieh=models.IntegerField(null=True,blank=True)
    rent=models.IntegerField(null=True,blank=True)
    
    publisher=models.CharField(max_length=200,null=True,blank=True,choices=PUBLISHER_CHOICES,default="شخصی")
    floor=models.IntegerField(null=True,blank=True)
    detail=models.TextField(max_length=450,null=True,blank=True)
    parking=models.BooleanField(default=False)
    anbari=models.BooleanField(default=False)
    sanad_adari=models.CharField(max_length=200,null=True,blank=True,choices=COVERSIMCART,default="ندارد")

    # وسایل نقلیه
    karkard_mashin=models.IntegerField(null=True,blank=True)
    day_rent_paid=models.IntegerField(null=True,blank=True)
    production_year=models.IntegerField(null=True,blank=True)
    color=models.CharField(max_length=100,null=True,blank=True,choices=COLORS,default="همه")
    brand_or_tip=models.CharField(max_length=100,null=True,blank=True)
    brand_or_tip=models.CharField(max_length=100,null=True,blank=True)
    fuel_type=models.CharField(max_length=100,null=True,blank=True,choices=FUEL_CHOICES)
    engin_type=models.CharField(max_length=100,null=True,blank=True,choices=ENGIN_TYPE)
    shasti_type=models.CharField(max_length=100,null=True,blank=True,choices=ENGIN_TYPE)
    body_type=models.CharField(max_length=100,null=True,blank=True,choices=BODY_STATUS)
    insurance_time=models.IntegerField(null=True,blank=True)
    girbox=models.CharField(max_length=100,null=True,blank=True,choices=TRANSMITION_TYPE)
    publisherForCar=models.CharField(max_length=200,null=True,blank=True,choices=PUBLISHERForCar_CHOICES,default="همه")
    internal_or_external=models.CharField(max_length=200,null=True,blank=True,choices=INTERNALOREXTERNAL,default="همه")
    

    # کالاهای دیجیتال
    phone_status=models.CharField(max_length=100,null=True,blank=True,choices=PHONE_STATUS,default="همه")
    esalat=models.CharField(max_length=100,null=True,blank=True,choices=ORIGINAL_OR_NOT,default="همه")
    sim_cart_number=models.IntegerField(null=True,blank=True)
    memory_size=models.IntegerField(null=True,blank=True,choices=MEMORYSIZE,default=4)
    ram_size=models.IntegerField(null=True,blank=True)
    window_size=models.CharField(max_length=100,null=True,blank=True)
    os_typpe=models.CharField(max_length=100,null=True,blank=True)
    game_pad_number=models.IntegerField(null=True,blank=True)
    cover_simcart=models.CharField(max_length=100,null=True,blank=True,choices=COVERSIMCART,default="ندارد")
    simcartType=models.CharField(max_length=100,null=True,blank=True,choices=SIMCARTTYPE,default="ایرانسل")
    

    # وسایل شخصی 

    cloths_type=models.CharField(max_length=100,null=True,blank=True,choices=CLOSTHTYPE,default="همه")

    com_status=models.CharField(max_length=200,null=True,blank=True,choices=COMMERICAL_STATUS,default='عادی')

    #استخدام و کاریابی
    price_for_work=models.IntegerField(null=True,blank=True,default=0)
    
    farWork=models.BooleanField(default=False)
    soldier=models.BooleanField(default=False)
    insurance=models.BooleanField(default=False)

    
    created=models.DateTimeField(default=timezone.now)
    updated=models.DateTimeField(auto_now=True)

    # objects=CommericalManger()
    ready_to_exchange.bool=True
    def __str__(self):
        return self.title
    
    @property
    def children(self):
        return Commerical.objects.all().filter(
            parent=self
        )
    @property
    def is_parent(self):
        
        if self.parent is None:
            return True
        else:
            return False

    def is_parent2(self):
        
        if self.parent is None:
            return True
        else:
            return False
        
    @property
    def iranTimeCreated(self):
        return datetime2jalali(self.created)
    
    


    @property
    def iranTimeUpdated(self):
        return datetime2jalali(self.updated)
    
    @property
    def iranTimeCreated2(self):
        return date2jalali(self.created)

    @property
    def bg_red_for_cars(self):
        if self.parent:
            if self.parent.title=="سواری و وانت":
                return format_html(f'<p style="background-color:red;" >{self.title}</p>')

    @property
    def yellow_red_for_phones(self):
        if self.parent:
            if self.parent.title=="گوشی موبایل":
                return format_html(f'<p style="background-color:yellow;" >{self.title}</p>')


def comImagesPath(instance,filename):
    return f"{instance.commerical.title} + {instance.commerical.user.phone_number}/{filename}"


class CommericalImage(models.Model):

    image=models.ImageField(upload_to=comImagesPath,null=True,blank=True,validators=[FileExtensionValidator(allowed_extensions=["png","jpg","jpeg"])])
    commerical=models.ForeignKey(Commerical,on_delete=models.CASCADE)









class Thread(models.Model):

    commerical=models.ForeignKey(Commerical,on_delete=models.CASCADE,null=True,blank=True,related_name="commerical")
    sender=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name="sender")
    receiver=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name="receiver")

    # def __str__(self) -> str:
    #     return self.sender.username
    



class Message(models.Model):

    thread=models.ForeignKey(Thread,on_delete=models.CASCADE,null=True,blank=True,related_name="+")
    sender_user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name="sender_user")
    receiver_user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name="receiver_user")
    text=models.TextField(null=True)
    created=models.DateTimeField(default=timezone.now)
    
    def __str__(self) -> str:
        return self.text[:5]
    
    @property
    def iranTimeCreated(self):
        return datetime2jalali(self.created)

